# DearMe Frontend (minimal demo)

This folder contains a minimal Flutter demo showcasing a pale-pink theme and a blinking floral widget used by the `DashboardView`.

Run steps (on machine with Flutter installed):

1. Open a terminal and change to this folder:

```bash
cd frontend
```

2. Get dependencies:

```bash
flutter pub get
```

3. Run on an available device or emulator:

```bash
flutter run
```

If you want the backend running too, follow backend instructions in the repo root README. You will need Python, a PostgreSQL instance, and the `DATABASE_URL` env var set before starting the FastAPI server.
Frontend — Flutter Folder Structure (Clean Architecture + MVVM)

Suggested feature-based structure:

lib/
- core/
  - di/           # dependency injection setup (get_it / injectable)
  - network/      # API client, interceptors
  - ui/           # shared widgets, theme, styles
  - utils/        # helpers, validators
  - models/       # shared DTOs
- features/
  - onboarding/
    - data/       # repos, data sources
    - domain/     # usecases, entities
    - presentation/
      - viewmodels/
      - views/
  - dashboard/
  - health/
    - water/
    - sleep/
    - mood/
    - meals/
    - menstrual/
  - tasks/
  - goals/
  - calendar/
  - placement/
  - coding_tracker/
  - ai_companion/
- app.dart        # app bootstrap, providers (Riverpod)
- main.dart

Key libraries
- Riverpod (state management)
- GoRouter (navigation)
- FL Chart (analytics)
- Table Calendar
- Firebase Auth, Messaging

Notes
- Use Repository pattern to abstract network/local storage.
- ViewModels expose state via Riverpod providers.

Notes about visual assets and Lottie:
- This demo loads a Lottie animation from the network (an example in the dashboard). For production, download Lottie JSON files into `assets/` and reference them in `pubspec.yaml`.
- You can tune animations and add SVG assets under `assets/` as needed.
