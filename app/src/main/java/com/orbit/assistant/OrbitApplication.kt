package com.orbit.assistant

import android.app.Application
import com.orbit.assistant.data.engine.RealOrbitEngine
import com.orbit.assistant.data.remote.OmniRouteClient
import com.orbit.assistant.data.repository.ActivityRepositoryImpl
import com.orbit.assistant.data.repository.SettingsRepositoryImpl
import com.orbit.assistant.data.security.AndroidKeystoreSecureStorage
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.repository.ActivityRepository
import com.orbit.assistant.domain.repository.SecureStorage
import com.orbit.assistant.domain.repository.SettingsRepository
import com.orbit.assistant.domain.tools.GetCurrentTimeTool
import com.orbit.assistant.domain.tools.OpenAppTool
import com.orbit.assistant.domain.tools.OpenUrlTool
import com.orbit.assistant.domain.tools.SearchWebTool
import com.orbit.assistant.domain.tools.ToolRegistry
import com.orbit.assistant.service.voice.OrbitSpeechRecognizer
import com.orbit.assistant.service.voice.OrbitTextToSpeech

class OrbitApplication : Application() {

    lateinit var secureStorage: SecureStorage
        private set
    lateinit var omniRouteClient: OmniRouteClient
        private set
    lateinit var settingsRepository: SettingsRepository
        private set
    lateinit var activityRepository: ActivityRepository
        private set
    lateinit var toolRegistry: ToolRegistry
        private set
    lateinit var speechRecognizer: OrbitSpeechRecognizer
        private set
    lateinit var textToSpeech: OrbitTextToSpeech
        private set
    lateinit var orbitEngine: OrbitEngine
        private set

    override fun onCreate() {
        super.onCreate()

        // 1. Hardware Keystore backed storage
        secureStorage = AndroidKeystoreSecureStorage(this)

        // 2. OmniRoute OpenAI-compatible network client
        omniRouteClient = OmniRouteClient()

        // 3. Repositories
        settingsRepository = SettingsRepositoryImpl(
            context = this,
            secureStorage = secureStorage,
            omniRouteClient = omniRouteClient
        )
        activityRepository = ActivityRepositoryImpl()

        // 4. Secure Tool Registry (Zero arbitrary code execution)
        toolRegistry = ToolRegistry().apply {
            register(OpenAppTool(this@OrbitApplication))
            register(OpenUrlTool(this@OrbitApplication))
            register(GetCurrentTimeTool())
            register(SearchWebTool(this@OrbitApplication))
        }

        // 5. Native Voice Subsystems
        speechRecognizer = OrbitSpeechRecognizer(this)
        textToSpeech = OrbitTextToSpeech(this)

        // 6. Real Autonomous Agent Loop
        orbitEngine = RealOrbitEngine(
            omniRouteClient = omniRouteClient,
            settingsRepository = settingsRepository,
            activityRepository = activityRepository,
            toolRegistry = toolRegistry,
            onSpeak = { text -> textToSpeech.speak(text) }
        )
    }

    override fun onTerminate() {
        super.onTerminate()
        textToSpeech.shutdown()
    }
}
