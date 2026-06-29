import 'package:flutter/material.dart';
import 'core/ui/theme.dart';
import 'features/dashboard/view.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DearMe',
      theme: buildPalePinkTheme(),
      home: const DashboardView(),
      debugShowCheckedModeBanner: false,
    );
  }
}
