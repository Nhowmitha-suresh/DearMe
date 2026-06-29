import 'package:flutter/material.dart';
import '../../core/ui/widgets/floral_blink.dart';
import '../../core/ui/widgets/petals.dart';
import '../../core/ui/widgets/butterfly.dart';
import '../../core/ui/widgets/bloom_transition.dart';
import '../../core/ui/widgets/progress_ring.dart';
import '../../core/ui/widgets/glowing_button.dart';
import '../../core/ui/widgets/mascot.dart';
import 'package:lottie/lottie.dart';

class DashboardView extends StatelessWidget {
  const DashboardView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('DearMe')),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(colors: [Color(0xFFFFF8FA), Color(0xFFFFEAF0)], begin: Alignment.topCenter, end: Alignment.bottomCenter),
        ),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(height: 16),
                Stack(
                  alignment: Alignment.center,
                  children: const [
                    FloatingPetals(count: 10, width: 260),
                    FloralBlink(size: 170),
                    Butterfly(size: 84),
                  ],
                ),
                const SizedBox(height: 18),
                const BloomTransition(child: Text('Welcome to DearMe', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600))),
                const SizedBox(height: 18),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: const [AnimatedProgressRing(percent: 0.72, label: 'Focus')]),
                const SizedBox(height: 18),
                Lottie.network('https://assets10.lottiefiles.com/packages/lf20_touohxv0.json', width: 120, height: 120),
                const SizedBox(height: 12),
                GestureDetector(
                  onTap: () {},
                  child: GlowingButton(child: const Text('Start Session', style: TextStyle(fontWeight: FontWeight.bold)), onTap: () {}),
                ),
                const SizedBox(height: 18),
                const FloatingMascot(),
                const SizedBox(height: 36),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
