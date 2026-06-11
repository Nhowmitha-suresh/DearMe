import 'package:flutter/material.dart';

class AppTheme {
  // Pink Floral Color Palette
  static const Color primaryPink = Color(0xFFE91E63); // Deep pink
  static const Color lightPink = Color(0xFFF06292); // Medium pink
  static const Color palePink = Color(0xFFFCE4EC); // Very light pink
  static const Color flushPink = Color(0xFFFF69B4); // Hot pink
  static const Color roseGold = Color(0xFFB76E79); // Rose gold accent

  // Floral accents
  static const Color floraPeach = Color(0xFFFFB74D); // Peach
  static const Color floraPurple = Color(0xFFB39DDB); // Purple
  static const Color floraGreen = Color(0xFF81C784); // Soft green
  static const Color floraWhite = Color(0xFFFFFAF0); // Off-white/cream

  // Neutral colors
  static const Color darkText = Color(0xFF2C2C2C);
  static const Color mediumText = Color(0xFF666666);
  static const Color lightText = Color(0xFFB0B0B0);
  static const Color dividerColor = Color(0xFFF5F5F5);

  // Gradient
  static const LinearGradient flowerGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [lightPink, primaryPink],
  );

  static const LinearGradient softFlowerGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [palePink, floraWhite],
  );

  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.light(
      primary: primaryPink,
      secondary: lightPink,
      tertiary: roseGold,
      surface: floraWhite,
      error: Color(0xFFD32F2F),
      onPrimary: Colors.white,
      onSecondary: Colors.white,
      onSurface: darkText,
    ),
    scaffoldBackgroundColor: floraWhite,
    appBarTheme: AppBarTheme(
      backgroundColor: floraWhite,
      surfaceTintColor: floraWhite,
      elevation: 0,
      centerTitle: true,
      iconThemeData: IconThemeData(color: primaryPink),
      titleTextStyle: TextStyle(
        color: darkText,
        fontSize: 20,
        fontWeight: FontWeight.bold,
      ),
    ),
    cardTheme: CardTheme(
      color: Colors.white,
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    ),
    buttonTheme: ButtonThemeData(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: primaryPink,
        foregroundColor: Colors.white,
        padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        textStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: primaryPink,
        textStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: primaryPink,
        side: BorderSide(color: lightPink, width: 1.5),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        textStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Color(0xFFFFF5F8),
      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: palePink),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: palePink, width: 1),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: primaryPink, width: 2),
      ),
      labelStyle: TextStyle(color: mediumText),
      hintStyle: TextStyle(color: lightText),
      prefixIconColor: primaryPink,
      suffixIconColor: primaryPink,
    ),
    textTheme: TextTheme(
      displayLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: darkText,
      ),
      displayMedium: TextStyle(
        fontSize: 28,
        fontWeight: FontWeight.bold,
        color: darkText,
      ),
      displaySmall: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: darkText,
      ),
      headlineMedium: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        color: darkText,
      ),
      headlineSmall: TextStyle(
        fontSize: 18,
        fontWeight: FontWeight.w600,
        color: darkText,
      ),
      titleLarge: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w600,
        color: darkText,
      ),
      titleMedium: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        color: darkText,
      ),
      titleSmall: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        color: mediumText,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        color: darkText,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        color: darkText,
      ),
      bodySmall: TextStyle(
        fontSize: 12,
        color: mediumText,
      ),
      labelLarge: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        color: Colors.white,
      ),
    ),
    floatingActionButtonTheme: FloatingActionButtonThemeData(
      backgroundColor: primaryPink,
      foregroundColor: Colors.white,
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: palePink,
      selectedColor: primaryPink,
      labelStyle: TextStyle(color: darkText),
      secondaryLabelStyle: TextStyle(color: Colors.white),
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      side: BorderSide.none,
    ),
    bottomNavigationBarTheme: BottomNavigationBarThemeData(
      backgroundColor: Colors.white,
      selectedItemColor: primaryPink,
      unselectedItemColor: lightText,
      elevation: 8,
      type: BottomNavigationBarType.fixed,
    ),
    dividerTheme: DividerThemeData(
      color: dividerColor,
      thickness: 1,
      space: 16,
    ),
  );
}

// Extension for easy color access
extension FlowerTheme on BuildContext {
  Color get primaryPink => AppTheme.primaryPink;
  Color get lightPink => AppTheme.lightPink;
  Color get palePink => AppTheme.palePink;
  Color get floraWhite => AppTheme.floraWhite;
}
