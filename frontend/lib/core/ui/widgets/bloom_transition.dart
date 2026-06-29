import 'package:flutter/material.dart';

class BloomTransition extends StatefulWidget {
  final Widget child;
  final Duration duration;
  const BloomTransition({Key? key, required this.child, this.duration = const Duration(milliseconds: 650)}) : super(key: key);

  @override
  State<BloomTransition> createState() => _BloomTransitionState();
}

class _BloomTransitionState extends State<BloomTransition> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: widget.duration)..forward();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: CurvedAnimation(parent: _ctrl, curve: Curves.elasticOut),
      child: FadeTransition(opacity: _ctrl, child: widget.child),
    );
  }
}
