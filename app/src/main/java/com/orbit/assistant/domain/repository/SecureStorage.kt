package com.orbit.assistant.domain.repository

interface SecureStorage {
    suspend fun getApiKey(): String?
    suspend fun saveApiKey(apiKey: String)
    suspend fun clearApiKey()
    suspend fun hasApiKey(): Boolean
}
