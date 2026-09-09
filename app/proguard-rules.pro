# Keep data models for kotlinx.serialization and OkHttp
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
-keepclassmembers class * {
    @kotlinx.serialization.Serializable <fields>;
}

# Android Security Crypto
-keepclassmembers class androidx.security.crypto.** { *; }
