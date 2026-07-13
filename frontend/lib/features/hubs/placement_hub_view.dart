import 'package:flutter/material.dart';

class PlacementHubView extends StatefulWidget {
  const PlacementHubView({super.key});

  @override
  State<PlacementHubView> createState() => _PlacementHubViewState();
}

class _PlacementHubViewState extends State<PlacementHubView> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Mock student details
  final String _studentName = "Aman Sharma";
  final String _department = "Computer Science";
  final double _cgpa = 9.1;
  final List<String> _skills = ["Flutter", "FastAPI", "Python", "SQL", "DSA"];
  final List<String> _targetRoles = ["Software Development Engineer", "Backend Developer"];

  // Mock companies list
  final List<Map<String, dynamic>> _companies = [
    {
      "name": "Google",
      "role": "Software Engineering Intern",
      "package": "₹1,50,000 / month",
      "location": "Bangalore, India",
      "deadline": "July 25, 2026",
      "logo": "G",
      "color": const Color(0xFF4285F4),
    },
    {
      "name": "Microsoft",
      "role": "Software Engineer (Full-Time)",
      "package": "₹28,00,000 / year",
      "location": "Hyderabad, India",
      "deadline": "July 30, 2026",
      "logo": "M",
      "color": const Color(0xFFF25022),
    },
    {
      "name": "Meta",
      "role": "Production Engineer",
      "package": "₹32,00,000 / year",
      "location": "Remote / London",
      "deadline": "August 05, 2026",
      "logo": "∞",
      "color": const Color(0xFF0081FB),
    },
    {
      "name": "Stripe",
      "role": "Backend Engineer (SDE I)",
      "package": "₹24,00,000 / year",
      "location": "Bangalore, India",
      "deadline": "August 12, 2026",
      "logo": "S",
      "color": const Color(0xFF635BFF),
    },
  ];

  // Active student applications tracker
  final List<Map<String, dynamic>> _applications = [
    {
      "company": "Google",
      "role": "Software Engineering Intern",
      "status": "Online Assessment", // Status values: Applied, OA, Interviewing, Offered, Rejected
      "appliedDate": "July 10, 2026",
      "color": const Color(0xFF4285F4),
    },
    {
      "company": "Stripe",
      "role": "Backend Engineer (SDE I)",
      "status": "Applied",
      "appliedDate": "July 12, 2026",
      "color": const Color(0xFF635BFF),
    },
  ];

  // Mock interview feedback logs
  final List<Map<String, dynamic>> _mockInterviews = [
    {
      "topic": "System Design & Databases",
      "rating": 4,
      "date": "July 08, 2026",
      "feedback": "Great understanding of SQL scaling and replicas. Work on caching write-through strategies."
    },
    {
      "topic": "Data Structures (Graphs/Trees)",
      "rating": 5,
      "date": "July 11, 2026",
      "feedback": "Perfect traversal solutions for multi-way trees. Highly articulate explanation."
    }
  ];

  final _mockTopicCtrl = TextEditingController();
  int _mockRating = 4;
  final _mockFeedbackCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _mockTopicCtrl.dispose();
    _mockFeedbackCtrl.dispose();
    super.dispose();
  }

  void _applyToCompany(Map<String, dynamic> comp) {
    // Check if already applied
    final exists = _applications.any((app) => app["company"] == comp["name"]);
    if (exists) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("You have already logged an application for ${comp["name"]}"),
          backgroundColor: Colors.amber.shade900,
        ),
      );
      return;
    }

    setState(() {
      _applications.add({
        "company": comp["name"],
        "role": comp["role"],
        "status": "Applied",
        "appliedDate": "Today",
        "color": comp["color"],
      });
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("Applied successfully to ${comp["name"]}! Check your pipeline."),
        backgroundColor: const Color(0xFF00796B),
      ),
    );
  }

  void _updateStatus(int idx, String nextStatus) {
    setState(() {
      _applications[idx]["status"] = nextStatus;
    });
  }

  void _logMockInterview() {
    if (_mockTopicCtrl.text.isNotEmpty && _mockFeedbackCtrl.text.isNotEmpty) {
      setState(() {
        _mockInterviews.insert(0, {
          "topic": _mockTopicCtrl.text,
          "rating": _mockRating,
          "date": "Today",
          "feedback": _mockFeedbackCtrl.text,
        });
        _mockTopicCtrl.clear();
        _mockFeedbackCtrl.clear();
      });
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Mock interview session logged. Spirit Nadhi notes your effort."),
          backgroundColor: Color(0xFF00796B),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5FAF9),
      appBar: AppBar(
        title: const Text('PLACEMENT HUB'),
        bottom: TabBar(
          controller: _tabController,
          labelColor: const Color(0xFF006A7A),
          unselectedLabelColor: Colors.grey,
          indicatorColor: const Color(0xFF00ACC1),
          tabs: const [
            Tab(text: "JOBS", icon: Icon(Icons.business)),
            Tab(text: "PIPELINE", icon: Icon(Icons.trending_up)),
            Tab(text: "PREP LAB", icon: Icon(Icons.insights)),
          ],
        ),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFF2FAF9), Color(0xFFE5F4F3)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: TabBarView(
          controller: _tabController,
          children: [
            _buildJobsTab(),
            _buildPipelineTab(),
            _buildPrepTab(),
          ],
        ),
      ),
    );
  }

  // TAB 1: Companies & Jobs Visiting
  Widget _buildJobsTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Profile Summary Panel
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(
                  color: Colors.teal.shade900.withValues(alpha: 0.04),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _studentName,
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF004D5A)),
                        ),
                        Text("CGPA: $_cgpa • $_department", style: const TextStyle(color: Colors.grey, fontSize: 13)),
                      ],
                    ),
                    const CircleAvatar(
                      backgroundColor: Color(0xFFE0F2F1),
                      child: Icon(Icons.person, color: Color(0xFF007A87)),
                    ),
                  ],
                ),
                const Divider(height: 24),
                const Text("Target Roles", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF004D5A))),
                const SizedBox(height: 4),
                Wrap(
                  spacing: 6,
                  children: _targetRoles.map((r) => Chip(
                    label: Text(r, style: const TextStyle(fontSize: 10, color: Color(0xFF004D5A))),
                    backgroundColor: const Color(0xFFB2DFDB).withValues(alpha: 0.4),
                    padding: EdgeInsets.zero,
                    visualDensity: VisualDensity.compact,
                  )).toList(),
                ),
                const SizedBox(height: 8),
                const Text("Skills", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF004D5A))),
                const SizedBox(height: 4),
                Wrap(
                  spacing: 6,
                  children: _skills.map((s) => Chip(
                    label: Text(s, style: const TextStyle(fontSize: 10, color: Color(0xFF007A87))),
                    backgroundColor: const Color(0xFFE0F7FA),
                    padding: EdgeInsets.zero,
                    visualDensity: VisualDensity.compact,
                  )).toList(),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          
          const Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("Visiting Companies", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF004D5A))),
              Icon(Icons.filter_list, color: Color(0xFF00ACC1), size: 20),
            ],
          ),
          const SizedBox(height: 12),

          // Company Listings
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _companies.length,
            itemBuilder: (context, idx) {
              final c = _companies[idx];
              return Card(
                margin: const EdgeInsets.only(bottom: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
                elevation: 1.5,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          CircleAvatar(
                            radius: 22,
                            backgroundColor: (c["color"] as Color).withValues(alpha: 0.12),
                            child: Text(
                              c["logo"],
                              style: TextStyle(color: c["color"], fontWeight: FontWeight.bold, fontSize: 20),
                            ),
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(c["role"], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                                Text(c["name"], style: TextStyle(color: c["color"], fontWeight: FontWeight.w600, fontSize: 13)),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          const Icon(Icons.monetization_on_outlined, size: 16, color: Colors.grey),
                          const SizedBox(width: 6),
                          Text(c["package"], style: const TextStyle(fontSize: 12, color: Colors.black87)),
                          const Spacer(),
                          const Icon(Icons.location_on_outlined, size: 16, color: Colors.grey),
                          const SizedBox(width: 6),
                          Text(c["location"], style: const TextStyle(fontSize: 12, color: Colors.black87)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text("Deadline: ${c["deadline"]}", style: const TextStyle(fontSize: 11, color: Colors.redAccent, fontWeight: FontWeight.bold)),
                          ElevatedButton(
                            onPressed: () => _applyToCompany(c),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF007A87),
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              minimumSize: Size.zero,
                              tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                            ),
                            child: const Text("Apply", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  // TAB 2: Applications Tracker Pipeline
  Widget _buildPipelineTab() {
    if (_applications.isEmpty) {
      return const Center(
        child: Text("No applications tracked. Go to JOBS tab to apply!"),
      );
    }

    final List<String> statuses = ["Applied", "Online Assessment", "Interviewing", "Offered", "Rejected"];

    return ListView.builder(
      padding: const EdgeInsets.all(16.0),
      itemCount: _applications.length,
      itemBuilder: (context, idx) {
        final app = _applications[idx];
        final currentStatus = app["status"];
        final color = app["color"];
        
        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(app["company"], style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: color)),
                        Text(app["role"], style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: currentStatus == "Offered" ? Colors.green.shade50 : (currentStatus == "Rejected" ? Colors.red.shade50 : Colors.teal.shade50),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: currentStatus == "Offered" ? Colors.green.shade200 : (currentStatus == "Rejected" ? Colors.red.shade200 : Colors.teal.shade200)),
                      ),
                      child: Text(
                        currentStatus.toUpperCase(),
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: currentStatus == "Offered" ? Colors.green.shade800 : (currentStatus == "Rejected" ? Colors.red.shade800 : Colors.teal.shade800),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                
                // Pipeline Progress Bar
                Row(
                  children: List.generate(4, (pIdx) {
                    final stepStatuses = ["Applied", "Online Assessment", "Interviewing", "Offered"];
                    final stepIndex = stepStatuses.indexOf(currentStatus);
                    final isComplete = stepIndex >= pIdx;
                    final isRejected = currentStatus == "Rejected";
                    
                    return Expanded(
                      child: Container(
                        height: 6,
                        margin: const EdgeInsets.symmetric(horizontal: 2),
                        decoration: BoxDecoration(
                          color: isRejected
                              ? Colors.red.shade300
                              : (isComplete ? color : Colors.grey.shade200),
                          borderRadius: BorderRadius.circular(3),
                        ),
                      ),
                    );
                  }),
                ),
                const SizedBox(height: 16),

                // Update pipeline status selector
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text("Applied: ${app["appliedDate"]}", style: const TextStyle(fontSize: 11, color: Colors.grey)),
                    PopupMenuButton<String>(
                      onSelected: (newStatus) => _updateStatus(idx, newStatus),
                      itemBuilder: (context) {
                        return statuses.map((status) => PopupMenuItem(
                          value: status,
                          child: Text(status),
                        )).toList();
                      },
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.shade300),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Row(
                          children: [
                            Text("Update Status", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF007A87))),
                            SizedBox(width: 4),
                            Icon(Icons.arrow_drop_down, size: 16, color: Color(0xFF007A87)),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  // TAB 3: Placement Preparation Lab
  Widget _buildPrepTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Preparation Progress Cards
          Row(
            children: [
              Expanded(
                child: _buildMetricCard("DSA Solved", "148 Problems", Icons.code, Colors.orange),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildMetricCard("Mock Score", "84% Readiness", Icons.analytics, Colors.teal),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Spirit Nadhi Resume Checker Tip
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFFE0F2F1), Color(0xFFB2DFDB)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(20),
            ),
            child: const Row(
              children: [
                Icon(Icons.water, color: Color(0xFF00796B), size: 32),
                SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text("Spirit Nadhi Feedback", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF004D40), fontSize: 14)),
                      SizedBox(height: 4),
                      Text(
                        "\"Your coding stream is flowing with focus today. Keep solved DSA topics active on LeetCode; it forms the bedrock for Microsoft and Stripe tests next week.\"",
                        style: TextStyle(fontStyle: FontStyle.italic, color: Color(0xFF00695C), fontSize: 12, height: 1.3),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Mock Interviews Header
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Mock Interview Log", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF004D5A))),
              ElevatedButton.icon(
                onPressed: _showAddMockDialog,
                icon: const Icon(Icons.add, size: 16, color: Colors.white),
                label: const Text("Log Mock", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF00ACC1),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  minimumSize: Size.zero,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Mock Interview Log List
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _mockInterviews.length,
            itemBuilder: (context, idx) {
              final mock = _mockInterviews[idx];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                shape: const RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(16))),
                child: Padding(
                  padding: const EdgeInsets.all(14.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(mock["topic"], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B))),
                          Text(mock["date"], style: const TextStyle(fontSize: 11, color: Colors.grey)),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: List.generate(5, (starIdx) {
                          return Icon(
                            starIdx < mock["rating"] ? Icons.star : Icons.star_border,
                            color: Colors.amber,
                            size: 16,
                          );
                        }),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        mock["feedback"],
                        style: TextStyle(color: Colors.grey.shade800, fontSize: 12, height: 1.3),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMetricCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 10),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 8),
          Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey)),
          const SizedBox(height: 2),
          Text(value, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: Color(0xFF004D5A))),
        ],
      ),
    );
  }

  void _showAddMockDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
              title: const Text("Log Mock Interview", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF004D5A))),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextField(
                      controller: _mockTopicCtrl,
                      decoration: const InputDecoration(
                        labelText: "Topic (e.g. Algorithms)",
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Text("Rating", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 6),
                    Row(
                      children: List.generate(5, (idx) {
                        return IconButton(
                          padding: EdgeInsets.zero,
                          constraints: const BoxConstraints(),
                          icon: Icon(
                            idx < _mockRating ? Icons.star : Icons.star_border,
                            color: Colors.amber,
                          ),
                          onPressed: () {
                            setDialogState(() {
                              _mockRating = idx + 1;
                            });
                          },
                        );
                      }),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _mockFeedbackCtrl,
                      maxLines: 3,
                      decoration: const InputDecoration(
                        labelText: "Nadhi Reflections / Feedback",
                      ),
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text("Cancel"),
                ),
                ElevatedButton(
                  onPressed: _logMockInterview,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF00ACC1),
                    foregroundColor: Colors.white,
                  ),
                  child: const Text("Save Log"),
                ),
              ],
            );
          },
        );
      },
    );
  }
}
