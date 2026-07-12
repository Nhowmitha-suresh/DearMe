import 'package:flutter/material.dart';
import '../../core/ui/widgets/river_painter.dart';
import '../../core/ui/widgets/glowing_button.dart';
import '../../core/ui/widgets/mascot.dart';

class DashboardView extends StatefulWidget {
  const DashboardView({Key? key}) : super(key: key);

  @override
  State<DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  // Mock river state variables (would be fetched from the backend in production)
  double flowRate = 1.2;
  double clarity = 0.9;
  double floraDensity = 0.8;
  int wildlifeCount = 6;
  int activeBridges = 2;
  String weather = "sunny";
  String timeOfDay = "Morning";

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final size = MediaQuery.of(context).size;

    return Scaffold(
      appBar: AppBar(
        title: const Text('NADHI'),
        actions: [
          IconButton(
            icon: const Icon(Icons.wb_sunny_outlined, color: Color(0xFFE0A96D)),
            onPressed: () {},
          ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFF2FAF9), Color(0xFFE5F4F3)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 12),
              // Weather & Atmosphere Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "$timeOfDay Flow",
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF6B8B88),
                        ),
                      ),
                      const Text(
                        "Your Life's River",
                        style: TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF004D5A),
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, py: 6),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.teal.shade50.withOpacity(0.5),
                          blurRadius: 6,
                          spreadRadius: 1,
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.wb_twighlight, size: 18, color: Color(0xFF00ACC1)),
                        const SizedBox(width: 6),
                        Text(
                          weather.toUpperCase(),
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF007A87),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              // The Live River Canvas Container
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.teal.shade900.withOpacity(0.08),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                clipBehavior: Clip.antiAlias,
                child: Column(
                  children: [
                    Stack(
                      children: [
                        // Live Wave Simulation
                        RiverFlowWidget(
                          flowRate: flowRate,
                          clarity: clarity,
                          height: 160.0,
                        ),
                        // Overlay Stats
                        Positioned(
                          top: 16,
                          left: 16,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, py: 4),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.water, size: 14, color: Colors.white),
                                const SizedBox(width: 4),
                                Text(
                                  "Clarity: ${(clarity * 100).toInt()}%",
                                  style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600),
                                ),
                              ],
                            ),
                          ),
                        ),
                        Positioned(
                          top: 16,
                          right: 16,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, py: 4),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.speed, size: 14, color: Colors.white),
                                const SizedBox(width: 4),
                                Text(
                                  "Current: ${flowRate}x",
                                  style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _buildRiverFact(Icons.local_florist, "${(floraDensity * 100).toInt()}% Flora", "Banks"),
                          _buildRiverFact(Icons.pets, "$wildlifeCount Animals", "Forests"),
                          _buildRiverFact(Icons.edit_road, "$activeBridges Bridges", "Career Labs"),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Spirit Conversation Card (Nadhi Companion)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFE0F2F1), Color(0xFFB2DFDB)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  children: [
                    const FloatingMascot(size: 64),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            "Spirit Nadhi",
                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF004D40)),
                          ),
                          const SizedBox(height: 4),
                          const Text(
                            "\"Your current is steady today. The focus of your morning study has carved a deep, clear channel. Let's keep this flow going.\"",
                            style: TextStyle(fontSize: 13, fontStyle: FontStyle.italic, color: Color(0xFF00695C), height: 1.3),
                          ),
                          const SizedBox(height: 8),
                          GestureDetector(
                            onTap: () {},
                            child: const Text(
                              "Tap to talk to Nadhi →",
                              style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF00796B)),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Growth Ecosystem Map (Traditional Dashboard Replacements)
              const Text(
                "Personal Growth World",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF004D5A),
                ),
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                mainAxisSpacing: 16,
                crossAxisSpacing: 16,
                childAspectRatio: 1.15,
                children: [
                  _buildEcosystemCard(
                    context,
                    "Academic Center",
                    "Library & Classes",
                    "120m focused",
                    Icons.account_balance,
                    const Color(0xFF0077B6),
                    const Color(0xFF90E0EF),
                  ),
                  _buildEcosystemCard(
                    context,
                    "Innovation Lab",
                    "Github & Coding",
                    "14 commits today",
                    Icons.code,
                    const Color(0xFF009688),
                    const Color(0xFF80CBC4),
                  ),
                  _buildEcosystemCard(
                    context,
                    "Ecosystem Forest",
                    "Sleep & Restoration",
                    "7h 45m good sleep",
                    Icons.park,
                    const Color(0xFF2E7D32),
                    const Color(0xFFA5D6A7),
                  ),
                  _buildEcosystemCard(
                    context,
                    "Ecosystem Gardens",
                    "Hydration & Mood",
                    "1,800ml logged",
                    Icons.spa,
                    const Color(0xFFEF6C00),
                    const Color(0xFFFFCC80),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Action buttons
              Center(
                child: GlowingButton(
                  child: const Text(
                    'Chat with Nadhi',
                    style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                  onTap: () {},
                ),
              ),
              const SizedBox(height: 36),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRiverFact(IconData icon, String title, String subtitle) {
    return Column(
      children: [
        Icon(icon, color: const Color(0xFF00838F), size: 20),
        const SizedBox(height: 4),
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF004D40))),
        Text(subtitle, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ],
    );
  }

  Widget _buildEcosystemCard(
    BuildContext context,
    String title,
    String subtitle,
    String metric,
    IconData icon,
    Color primaryColor,
    Color secondaryColor,
  ) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: primaryColor.withOpacity(0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: primaryColor.withOpacity(0.12), width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: secondaryColor.withOpacity(0.3),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, color: primaryColor, size: 20),
              ),
              const Icon(Icons.arrow_forward_ios, size: 12, color: Colors.grey),
            ],
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: const TextStyle(fontSize: 10, color: Colors.grey),
              ),
            ],
          ),
          Text(
            metric,
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: primaryColor),
          ),
        ],
      ),
    );
  }
}
