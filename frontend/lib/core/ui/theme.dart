import 'package:flutter/material.dart';

ThemeData buildPalePinkTheme() {
  const primary = Color(0xFFFFE6EE); // pale pink
  const accent = Color(0xFFFFCFE6);

  return ThemeData(
    primaryColor: primary,
    colorScheme: ColorScheme.fromSeed(seedColor: accent, primary: primary),
    scaffoldBackgroundColor: const Color(0xFFFFF8FA),
    appBarTheme: const AppBarTheme(
      backgroundColor: primary,
      foregroundColor: Colors.black87,
      elevation: 0,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(backgroundColor: accent),
    splashFactory: InkRipple.splashFactory,
  );
}
