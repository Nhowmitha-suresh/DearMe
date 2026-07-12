import 'package:flutter/material.dart';

ThemeData buildNadhiNatureTheme() {
  const primary = Color(0xFF006A7A); // Deep Calming Teal
  const secondary = Color(0xFF00A896); // Soft River Teal
  const background = Color(0xFFF5FAF9); // Water-light background

  return ThemeData(
    useMaterial3: true,
    primaryColor: primary,
    colorScheme: ColorScheme.fromSeed(
      seedColor: secondary,
      primary: primary,
      secondary: secondary,
      surface: Colors.white,
    ),
    scaffoldBackgroundColor: background,
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.transparent,
      foregroundColor: Color(0xFF052B30),
      elevation: 0,
      centerTitle: true,
      titleTextStyle: TextStyle(
          fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF052B30)),
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: secondary,
      foregroundColor: Colors.white,
    ),
    splashFactory: InkRipple.splashFactory,
  );
}

ThemeData buildPalePinkTheme() => buildNadhiNatureTheme();
