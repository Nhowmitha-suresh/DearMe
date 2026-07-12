import 'package:flutter/material.dart';
import '../../core/ui/widgets/logo.dart';
import '../../core/ui/widgets/river_painter.dart';

class WelcomeView extends StatelessWidget {
  const WelcomeView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xFF00303F), // Deep River Night Blue
              Color(0xFF005b66), // Deep Calm Teal
              Color(0xFF00ACC1), // Active River Teal
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Stack(
          children: [
            // Wave overlay at the bottom
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Opacity(
                opacity: 0.65,
                child: RiverFlowWidget(
                  flowRate: 0.75,
                  clarity: 0.9,
                  height: MediaQuery.of(context).size.height * 0.35,
                ),
              ),
            ),
            // Floating sparkles or circles for atmosphere
            Positioned.fill(
              child: CustomPaint(
                painter: _WelcomeAtmospherePainter(),
              ),
            ),
            // Main content
            SafeArea(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const SizedBox(height: 20),
                      // Logo & Titles Group
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const NadhiLogo(size: 150),
                          const SizedBox(height: 32),
                          const Text(
                            "NADHI",
                            style: TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.w900,
                              letterSpacing: 8.0,
                              color: Colors.white,
                              shadows: [
                                Shadow(
                                  color: Colors.black38,
                                  offset: Offset(0, 4),
                                  blurRadius: 8,
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 12),
                          Container(
                            height: 2,
                            width: 80,
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(
                                colors: [Colors.transparent, Color(0xFF80DEEA), Colors.transparent],
                              ),
                              borderRadius: BorderRadius.circular(1),
                            ),
                          ),
                          const SizedBox(height: 16),
                          const Text(
                            "Your Life's River",
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w500,
                              letterSpacing: 2.0,
                              color: Color(0xFFB2DFDB),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            "Ecosystem Companion & Placement Navigator",
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 13,
                              color: Colors.white.withOpacity(0.65),
                              height: 1.4,
                            ),
                          ),
                        ],
                      ),
                      
                      // Action Buttons Group
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          // Glassmorphic log in button
                          SizedBox(
                            width: double.infinity,
                            height: 56,
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.white,
                                foregroundColor: const Color(0xFF004D5A),
                                elevation: 4,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(20),
                                ),
                              ),
                              onPressed: () {
                                Navigator.of(context).pushNamed('/login', arguments: false);
                              },
                              child: const Text(
                                "LOG IN TO FLOW",
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 1.5,
                                  fontSize: 15,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          // Transparent/outlined sign up button
                          SizedBox(
                            width: double.infinity,
                            height: 56,
                            child: OutlinedButton(
                              style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.white,
                                side: const BorderSide(color: Colors.white, width: 1.5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(20),
                                ),
                              ),
                              onPressed: () {
                                Navigator.of(context).pushNamed('/login', arguments: true);
                              },
                              child: const Text(
                                "BEGIN NEW CHANNEL (SIGN UP)",
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 1.5,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 36),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _WelcomeAtmospherePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.white.withOpacity(0.04)
      ..style = PaintingStyle.fill;
      
    // Draw some large background glowing circles
    canvas.drawCircle(Offset(size.width * 0.1, size.height * 0.2), 120, paint);
    canvas.drawCircle(Offset(size.width * 0.9, size.height * 0.45), 180, paint);
    canvas.drawCircle(Offset(size.width * 0.3, size.height * 0.75), 150, paint..color = const Color(0xFF00ACC1).withOpacity(0.06));
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
