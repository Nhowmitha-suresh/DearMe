import 'package:flutter/material.dart';
import 'core/ui/theme.dart';
import 'features/auth/welcome_view.dart';
import 'features/auth/login_view.dart';
import 'features/auth/customization_view.dart';
import 'features/dashboard/view.dart';
import 'features/hubs/placement_hub_view.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nadhi',
      theme: buildNadhiNatureTheme(),
      initialRoute: '/welcome',
      routes: {
        '/welcome': (context) => const WelcomeView(),
        '/login': (context) => const LoginView(),
        '/customization': (context) => const CustomizationView(),
        '/dashboard': (context) => const DashboardView(),
        '/placement': (context) => const PlacementHubView(),
      },
      debugShowCheckedModeBanner: false,
    );
  }
}
