import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:dearme_frontend/app.dart';

void main() {
  testWidgets('Dashboard smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the title 'NADHI' is rendered successfully in the app bar.
    expect(find.text('NADHI'), findsOneWidget);
    
    // Verify that the personal growth dashboard section is visible.
    expect(find.text("Your Life's River"), findsOneWidget);
  });
}
