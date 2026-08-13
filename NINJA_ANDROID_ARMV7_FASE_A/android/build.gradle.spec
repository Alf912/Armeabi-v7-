# Android build target — design specification
# This file is intentionally descriptive during Phase E.
# ABI is fixed by Phase F, not here.

android {
    namespace "com.ninja.android"
    // compileSdk/minSdk/version are to be pinned during Phase F.
    defaultConfig {
        applicationId "com.ninja.android"
    }
}
