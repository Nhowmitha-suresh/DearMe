import 'package:flutter/material.dart';
import 'core/ui/theme.dart';
import 'core/router.dart';

void main() {
  runApp(const DearMeApp());
}

class DearMeApp extends StatelessWidget {
  const DearMeApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'DearMe',
      theme: AppTheme.lightTheme,
      routerConfig: AppRouter.router,
      debugShowCheckedModeBanner: false,
    );
  }
}
