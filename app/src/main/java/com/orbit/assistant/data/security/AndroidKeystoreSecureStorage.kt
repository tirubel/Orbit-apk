package com.orbit.assistant.data.security

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.orbit.assistant.domain.repository.SecureStorage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AndroidKeystoreSecureStorage(private val context: Context) : SecureStorage {

    private val masterKey: MasterKey by lazy {
        MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
    }

    private val sharedPreferences: SharedPreferences by lazy {
        try {
            EncryptedSharedPreferences.create(
                context,
                "orbit_secure_vault",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        } catch (e: Exception) {
            context.getSharedPreferences("orbit_secure_vault", Context.MODE_PRIVATE).edit().clear().apply()
            EncryptedSharedPreferences.create(
                context,
                "orbit_secure_vault",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        }
    }

    companion object {
        private const val KEY_OMNIROUTE_API_KEY = "k_omniroute_secret_token"
    }

    override suspend fun getApiKey(): String? = withContext(Dispatchers.IO) {
        sharedPreferences.getString(KEY_OMNIROUTE_API_KEY, null)?.takeIf { it.isNotBlank() }
    }

    override suspend fun saveApiKey(apiKey: String) = withContext(Dispatchers.IO) {
        sharedPreferences.edit()
            .putString(KEY_OMNIROUTE_API_KEY, apiKey.trim())
            .apply()
    }

    override suspend fun clearApiKey() = withContext(Dispatchers.IO) {
        sharedPreferences.edit()
            .remove(KEY_OMNIROUTE_API_KEY)
            .apply()
    }

    override suspend fun hasApiKey(): Boolean = withContext(Dispatchers.IO) {
        val key = sharedPreferences.getString(KEY_OMNIROUTE_API_KEY, null)
        !key.isNullOrBlank()
    }
}
