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
