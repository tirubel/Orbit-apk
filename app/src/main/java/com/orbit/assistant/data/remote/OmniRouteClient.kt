package com.orbit.assistant.data.remote

import com.orbit.assistant.domain.model.ChatCompletionRequest
import com.orbit.assistant.domain.model.ChatCompletionResponse
import com.orbit.assistant.domain.model.OmniRouteModelsResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.net.ConnectException
import java.net.SocketTimeoutException
import java.util.concurrent.TimeUnit

sealed class OmniRouteException(message: String, cause: Throwable? = null) : Exception(message, cause) {
    class NotRunning(cause: Throwable? = null) : OmniRouteException("OmniRoute is not running or unreachable at local endpoint.", cause)
    class InvalidApiKey : OmniRouteException("Invalid OmniRoute API key. Authorization rejected.")
    class ModelUnavailable(val modelName: String) : OmniRouteException("Model '$modelName' is currently unavailable on OmniRoute.")
    class ConnectionTimeout(cause: Throwable? = null) : OmniRouteException("Connection to OmniRoute timed out.", cause)
    class GenericError(message: String, cause: Throwable? = null) : OmniRouteException(message, cause)
}

class OmniRouteClient(
    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build(),
    private val json: Json = Json {
        ignoreUnknownKeys = true
        encodeDefaults = true
        isLenient = true
    }
) {
    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    suspend fun getModels(baseUrl: String, apiKey: String?): Result<List<String>> = withContext(Dispatchers.IO) {
        val sanitizedBase = baseUrl.trimEnd('/')
        val url = "$sanitizedBase/models"
        val requestBuilder = Request.Builder()
            .url(url)
            .get()

        if (!apiKey.isNullOrBlank()) {
            requestBuilder.header("Authorization", "Bearer $apiKey")
        }

        val request = requestBuilder.build()
        try {
            val response = client.newCall(request).execute()
            response.use { res ->
                if (res.code == 401 || res.code == 403) {
                    return@withContext Result.failure(OmniRouteException.InvalidApiKey())
                }
                if (!res.isSuccessful) {
                    val errBody = res.body?.string() ?: ""
                    return@withContext Result.failure(
                        OmniRouteException.GenericError("HTTP ${res.code}: $errBody")
                    )
                }
                val responseBody = res.body?.string() ?: ""
                val modelsResponse = json.decodeFromString<OmniRouteModelsResponse>(responseBody)
                val modelList = modelsResponse.data.map { it.id }.sorted()
                Result.success(modelList)
            }
        } catch (e: ConnectException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: SocketTimeoutException) {
            Result.failure(OmniRouteException.ConnectionTimeout(e))
        } catch (e: IOException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: Exception) {
            Result.failure(OmniRouteException.GenericError(e.localizedMessage ?: "Unknown network error", e))
        }
    }

    suspend fun createChatCompletion(
        baseUrl: String,
        apiKey: String?,
        requestData: ChatCompletionRequest
    ): Result<ChatCompletionResponse> = withContext(Dispatchers.IO) {
        val sanitizedBase = baseUrl.trimEnd('/')
        val url = "$sanitizedBase/chat/completions"
        val requestJson = json.encodeToString(ChatCompletionRequest.serializer(), requestData)
        val body = requestJson.toRequestBody(jsonMediaType)

        val requestBuilder = Request.Builder()
            .url(url)
            .post(body)

        if (!apiKey.isNullOrBlank()) {
            requestBuilder.header("Authorization", "Bearer $apiKey")
        }

        val request = requestBuilder.build()
        try {
            val response = client.newCall(request).execute()
            response.use { res ->
                if (res.code == 401 || res.code == 403) {
                    return@withContext Result.failure(OmniRouteException.InvalidApiKey())
                }
                if (res.code == 404) {
                    return@withContext Result.failure(OmniRouteException.ModelUnavailable(requestData.model))
                }
                if (!res.isSuccessful) {
                    val errBody = res.body?.string() ?: ""
                    return@withContext Result.failure(
                        OmniRouteException.GenericError("HTTP ${res.code}: $errBody")
                    )
                }
                val responseBody = res.body?.string() ?: ""
                val chatResponse = json.decodeFromString<ChatCompletionResponse>(responseBody)
                Result.success(chatResponse)
            }
        } catch (e: ConnectException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: SocketTimeoutException) {
            Result.failure(OmniRouteException.ConnectionTimeout(e))
        } catch (e: IOException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: Exception) {
            Result.failure(OmniRouteException.GenericError(e.localizedMessage ?: "Chat completion error", e))
        }
    }
}
