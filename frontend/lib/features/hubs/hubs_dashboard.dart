import 'package:flutter/material.dart';

class HubDetailsView extends StatefulWidget {
  final String hubType;
  const HubDetailsView({Key? key, required this.hubType}) : super(key: key);

  @override
  State<HubDetailsView> createState() => _HubDetailsViewState();
}

class _HubDetailsViewState extends State<HubDetailsView> {
  @override
  Widget build(BuildContext context) {
    String title = "";
    Widget body = const SizedBox();

    switch (widget.hubType.toLowerCase()) {
      case "academic":
        title = "Academic Center";
        body = const AcademicHubView();
        break;
      case "coding":
        title = "Innovation Lab";
        body = const CodingHubView();
        break;
      case "health":
        title = "Ecosystem Gardens";
        body = const HealthHubView();
        break;
      case "finance":
        title = "Finance Tracker";
        body = const FinanceHubView();
        break;
      case "journal":
        title = "Daily Journal";
        body = const JournalHubView();
        break;
      case "chat":
        title = "Spirit Nadhi";
        body = const NadhiAICompanionView();
        break;
      default:
        title = "Ecosystem Hub";
        body = const Center(child: Text("Select an ecosystem sector."));
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(title.toUpperCase()),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: body,
    );
  }
}

// ----------------------------------------------------
// ACADEMIC HUB VIEW
// ----------------------------------------------------
class AcademicHubView extends StatefulWidget {
  const AcademicHubView({Key? key}) : super(key: key);

  @override
  State<AcademicHubView> createState() => _AcademicHubViewState();
}

class _AcademicHubViewState extends State<AcademicHubView> {
  int focusTimeRemaining = 25 * 60; // 25 minutes Pomodoro
  bool isTimerRunning = false;

  void _toggleTimer() {
    setState(() {
      isTimerRunning = !isTimerRunning;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Pomodoro Timer Card
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                  colors: [Color(0xFF0077B6), Color(0xFF00B4D8)]),
              borderRadius: BorderRadius.circular(24),
            ),
            child: Column(
              children: [
                const Icon(Icons.timer, color: Colors.white, size: 36),
                const SizedBox(height: 12),
                const Text("Pomodoro Study Focus",
                    style: TextStyle(color: Colors.white70, fontSize: 13)),
                const SizedBox(height: 6),
                Text(
                  "${(focusTimeRemaining ~/ 60).toString().padLeft(2, '0')}:${(focusTimeRemaining % 60).toString().padLeft(2, '0')}",
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 44,
                      fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 18),
                ElevatedButton(
                  onPressed: _toggleTimer,
                  style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: const Color(0xFF0077B6)),
                  child: Text(isTimerRunning ? "PAUSE" : "START FOCUS SESSION"),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          const Text("Timetable Classes",
              style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF004D5A))),
          const SizedBox(height: 12),
          _buildTimetableItem("CS 301: Database Management Systems",
              "09:00 AM - 10:30 AM", "Room 402"),
          _buildTimetableItem("MATH 202: Linear Algebra", "11:00 AM - 12:30 PM",
              "Auditorium B"),
          _buildTimetableItem(
              "CS 305: Analysis of Algorithms", "02:00 PM - 03:30 PM", "Lab 2"),
        ],
      ),
    );
  }

  Widget _buildTimetableItem(String title, String time, String room) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListTile(
        leading: const CircleAvatar(
            backgroundColor: Color(0xFFE0F7FA),
            child: Icon(Icons.class_, color: Color(0xFF00ACC1))),
        title: Text(title,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        subtitle: Text("$time • $room"),
        trailing: const Icon(Icons.arrow_forward_ios, size: 12),
      ),
    );
  }
}

// ----------------------------------------------------
// CODING HUB VIEW
// ----------------------------------------------------
class CodingHubView extends StatefulWidget {
  const CodingHubView({Key? key}) : super(key: key);

  @override
  State<CodingHubView> createState() => _CodingHubViewState();
}

class _CodingHubViewState extends State<CodingHubView> {
  int solvedCount = 42;
  int commitCount = 105;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: _buildMetricCard("LeetCode", "$solvedCount solved",
                    Icons.code, const Color(0xFFFFA116)),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildMetricCard("GitHub", "$commitCount commits",
                    Icons.commit, const Color(0xFF24292E)),
              ),
            ],
          ),
          const SizedBox(height: 24),
          const Text("Coding Roadmaps & Targets",
              style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF004D5A))),
          const SizedBox(height: 12),
          _buildTaskProgress("Daily Challenge: Binary Search Trees", 0.5),
          _buildTaskProgress("Clean Code principles reading", 0.8),
          _buildTaskProgress("Construct React landing portfolio", 0.2),
        ],
      ),
    );
  }

  Widget _buildMetricCard(String title, String val, IconData icon, Color col) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 10)
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: col, size: 28),
          const SizedBox(height: 12),
          Text(title,
              style:
                  const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
          const SizedBox(height: 4),
          Text(val, style: const TextStyle(color: Colors.grey, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildTaskProgress(String label, double pct) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label,
                style:
                    const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
            const SizedBox(height: 10),
            LinearProgressIndicator(
                value: pct,
                backgroundColor: Colors.grey.shade100,
                color: const Color(0xFF00ACC1)),
          ],
        ),
      ),
    );
  }
}

// ----------------------------------------------------
// HEALTH HUB VIEW
// ----------------------------------------------------
class HealthHubView extends StatefulWidget {
  const HealthHubView({Key? key}) : super(key: key);

  @override
  State<HealthHubView> createState() => _HealthHubViewState();
}

class _HubWaterState {
  int ml = 1200;
}

class _HealthHubViewState extends State<HealthHubView> {
  final _state = _HubWaterState();

  void _addWater(int val) {
    setState(() {
      _state.ml += val;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: const Color(0xFFE0F7FA),
              borderRadius: BorderRadius.circular(24),
            ),
            child: Column(
              children: [
                const Icon(Icons.local_drink,
                    color: Color(0xFF0097A7), size: 36),
                const SizedBox(height: 8),
                const Text("Today's Hydration",
                    style: TextStyle(color: Color(0xFF006064), fontSize: 14)),
                const SizedBox(height: 6),
                Text("${_state.ml} / 2500 ml",
                    style: const TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF006064))),
                const SizedBox(height: 18),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: () => _addWater(250),
                      style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00ACC1),
                          foregroundColor: Colors.white),
                      child: const Text("+250ml"),
                    ),
                    ElevatedButton(
                      onPressed: () => _addWater(500),
                      style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00838F),
                          foregroundColor: Colors.white),
                      child: const Text("+500ml"),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          const Text("Menstrual Cycle tracker",
              style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF004D5A))),
          const SizedBox(height: 12),
          Card(
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: const ListTile(
              leading: Icon(Icons.calendar_month, color: Colors.pinkAccent),
              title: Text("Next Period cycle prediction",
                  style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text("Expected: July 28 (Confidence: 85%)"),
            ),
          ),
        ],
      ),
    );
  }
}

// ----------------------------------------------------
// FINANCE HUB VIEW
// ----------------------------------------------------
class FinanceHubView extends StatefulWidget {
  const FinanceHubView({Key? key}) : super(key: key);

  @override
  State<FinanceHubView> createState() => _FinanceHubViewState();
}

class _FinanceHubViewState extends State<FinanceHubView> {
  final List<Map<String, dynamic>> _expenses = [
    {"name": "Library Study snacks", "val": 15.50, "cat": "food"},
    {"name": "A4 Notes Paper Notebooks", "val": 12.00, "cat": "academic"},
    {"name": "LeetCode Premium subscription", "val": 35.00, "cat": "coding"},
  ];

  final _nameCtrl = TextEditingController();
  final _amountCtrl = TextEditingController();

  void _addExpense() {
    final amt = double.tryParse(_amountCtrl.text) ?? 0.0;
    if (_nameCtrl.text.isNotEmpty && amt > 0.0) {
      setState(() {
        _expenses
            .insert(0, {"name": _nameCtrl.text, "val": amt, "cat": "general"});
        _nameCtrl.clear();
        _amountCtrl.clear();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Logging inputs
          Row(
            children: [
              Expanded(
                child: TextField(
                    controller: _nameCtrl,
                    decoration:
                        const InputDecoration(labelText: "Expense Item")),
              ),
              const SizedBox(width: 12),
              SizedBox(
                width: 80,
                child: TextField(
                    controller: _amountCtrl,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(labelText: "Price")),
              ),
              IconButton(
                  onPressed: _addExpense,
                  icon: const Icon(Icons.add_circle,
                      color: Color(0xFF00ACC1), size: 32)),
            ],
          ),
          const SizedBox(height: 24),
          const Text("Expense History",
              style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF004D5A))),
          const SizedBox(height: 12),
          Expanded(
            child: ListView.builder(
              itemCount: _expenses.length,
              itemBuilder: (context, idx) {
                final e = _expenses[idx];
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: const CircleAvatar(
                        backgroundColor: Color(0xFFFFF3E0),
                        child:
                            Icon(Icons.monetization_on, color: Colors.orange)),
                    title: Text(e["name"]),
                    subtitle: Text(e["cat"]),
                    trailing: Text("\$${e["val"].toStringAsFixed(2)}",
                        style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

// ----------------------------------------------------
// JOURNAL VIEW
// ----------------------------------------------------
class JournalHubView extends StatefulWidget {
  const JournalHubView({Key? key}) : super(key: key);

  @override
  State<JournalHubView> createState() => _JournalHubViewState();
}

class _JournalHubViewState extends State<JournalHubView> {
  final List<Map<String, String>> _entries = [
    {
      "title": "Morning focus in the library",
      "content":
          "I studied linear algebra for two hours today. Feeling focused and ready for the midterm.",
      "mood": "calm"
    },
  ];

  final _titleCtrl = TextEditingController();
  final _contentCtrl = TextEditingController();

  void _saveEntry() {
    if (_contentCtrl.text.isNotEmpty) {
      setState(() {
        _entries.insert(0, {
          "title": _titleCtrl.text.isEmpty ? "Untitled Entry" : _titleCtrl.text,
          "content": _contentCtrl.text,
          "mood": "happy"
        });
        _titleCtrl.clear();
        _contentCtrl.clear();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          TextField(
              controller: _titleCtrl,
              decoration: const InputDecoration(labelText: "Journal Title")),
          const SizedBox(height: 12),
          TextField(
              controller: _contentCtrl,
              maxLines: 3,
              decoration:
                  const InputDecoration(labelText: "How was your day?")),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: _saveEntry,
            style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00ACC1),
                foregroundColor: Colors.white),
            child: const Text("Save Journal & Ask Nadhi for reflections"),
          ),
          const SizedBox(height: 20),
          Expanded(
            child: ListView.builder(
              itemCount: _entries.length,
              itemBuilder: (context, idx) {
                final je = _entries[idx];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(je["title"]!,
                                style: const TextStyle(
                                    fontWeight: FontWeight.bold, fontSize: 15)),
                            Chip(
                                label: Text(je["mood"]!),
                                backgroundColor: const Color(0xFFE0F2F1)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(je["content"]!,
                            style: const TextStyle(color: Colors.black87)),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

// ----------------------------------------------------
// AI CHAT COMPANION
// ----------------------------------------------------
class NadhiAICompanionView extends StatefulWidget {
  const NadhiAICompanionView({Key? key}) : super(key: key);

  @override
  State<NadhiAICompanionView> createState() => _NadhiAICompanionViewState();
}

class _NadhiAICompanionViewState extends State<NadhiAICompanionView> {
  final List<Map<String, String>> _messages = [
    {
      "sender": "nadhi",
      "text":
          "Greetings, traveler. I am Nadhi, the spirit of your life's river. The focus of your morning study has carved a deep channel today. How can I guide you?"
    },
  ];

  final _msgCtrl = TextEditingController();

  void _sendMessage() {
    if (_msgCtrl.text.isNotEmpty) {
      final txt = _msgCtrl.text;
      setState(() {
        _messages.add({"sender": "user", "text": txt});
        _msgCtrl.clear();
      });

      // Simulated companion reply
      Future.delayed(const Duration(milliseconds: 1200), () {
        if (mounted) {
          setState(() {
            _messages.add({
              "sender": "nadhi",
              "text":
                  "Every drop of effort counts. Continue flowing steady, and the flora will bloom along your path."
            });
          });
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: _messages.length,
            itemBuilder: (context, idx) {
              final m = _messages[idx];
              final isUser = m["sender"] == "user";
              return Align(
                alignment:
                    isUser ? Alignment.centerRight : Alignment.centerLeft,
                child: Container(
                  margin: const EdgeInsets.only(bottom: 12),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isUser
                        ? const Color(0xFF00ACC1)
                        : const Color(0xFFECEFF1),
                    borderRadius: BorderRadius.only(
                      topLeft: const Radius.circular(16),
                      topRight: const Radius.circular(16),
                      bottomLeft:
                          isUser ? const Radius.circular(16) : Radius.zero,
                      bottomRight:
                          isUser ? Radius.zero : const Radius.circular(16),
                    ),
                  ),
                  child: Text(
                    m["text"]!,
                    style: TextStyle(
                        color: isUser ? Colors.white : Colors.black87),
                  ),
                ),
              );
            },
          ),
        ),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: const BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: Color(0xFFECEFF1)))),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                    controller: _msgCtrl,
                    decoration: const InputDecoration(
                        hintText: "Whisper to Nadhi...",
                        border: InputBorder.none)),
              ),
              IconButton(
                  onPressed: _sendMessage,
                  icon: const Icon(Icons.send, color: Color(0xFF00ACC1))),
            ],
          ),
        ),
      ],
    );
  }
}
