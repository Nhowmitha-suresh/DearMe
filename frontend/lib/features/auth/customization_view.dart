import 'package:flutter/material.dart';
import '../../core/ui/widgets/glowing_button.dart';
import '../../core/ui/widgets/logo.dart';

class CustomizationView extends StatefulWidget {
  const CustomizationView({Key? key}) : super(key: key);

  @override
  State<CustomizationView> createState() => _CustomizationViewState();
}

class _CustomizationViewState extends State<CustomizationView> {
  final PageController _pageController = PageController();
  int _currentStep = 0;

  // Form Controllers
  final _firstNameCtrl = TextEditingController();
  final _lastNameCtrl = TextEditingController();
  final _rollNoCtrl = TextEditingController();
  final _collegeCtrl = TextEditingController();
  final _departmentCtrl = TextEditingController();
  final _gpaCtrl = TextEditingController();
  
  int _selectedYear = 3; // default 3rd year
  
  final _skillsCtrl = TextEditingController();
  final _rolesCtrl = TextEditingController();

  final List<String> _skillsList = [];
  final List<String> _rolesList = [];

  void _addSkill() {
    final skill = _skillsCtrl.text.trim();
    if (skill.isNotEmpty && !_skillsList.contains(skill)) {
      setState(() {
        _skillsList.add(skill);
        _skillsCtrl.clear();
      });
    }
  }

  void _addRole() {
    final role = _rolesCtrl.text.trim();
    if (role.isNotEmpty && !_rolesList.contains(role)) {
      setState(() {
        _rolesList.add(role);
        _rolesCtrl.clear();
      });
    }
  }

  void _nextPage() {
    if (_currentStep < 2) {
      setState(() {
        _currentStep++;
      });
      _pageController.animateToPage(
        _currentStep,
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    } else {
      _submitCustomization();
    }
  }

  void _prevPage() {
    if (_currentStep > 0) {
      setState(() {
        _currentStep--;
      });
      _pageController.animateToPage(
        _currentStep,
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    }
  }

  void _submitCustomization() {
    // In production, this would make an API call to /api/v1/users/profile
    // We will simulate success and navigate to the dashboard.
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("Placement course set! Welcome to Nadhi."),
        backgroundColor: Color(0xFF00796B),
      ),
    );
    Navigator.of(context).pushReplacementNamed('/dashboard');
  }

  @override
  Widget build(BuildContext context) {
    final List<String> stepTitles = [
      "Carving Your Source",
      "Deepening Your Flow",
      "Reaching the Ocean",
    ];

    final List<String> stepSubtitles = [
      "Let's get to know you first",
      "Tell us about your academic path",
      "Add your skills and placement targets",
    ];

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFF2FAF9), Color(0xFFE5F4F3)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              const SizedBox(height: 20),
              // Header with River theme step progress
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back_ios, color: Color(0xFF004D5A)),
                      onPressed: _currentStep > 0 ? _prevPage : () => Navigator.of(context).pop(),
                    ),
                    const NadhiLogo(size: 44, animate: false),
                    const SizedBox(width: 48), // Spacer
                  ],
                ),
              ),
              const SizedBox(height: 16),
              // River Progress bar
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 32.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: List.generate(3, (idx) {
                        final isActive = idx <= _currentStep;
                        return Text(
                          "Step ${idx + 1}",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: isActive ? const Color(0xFF007A87) : Colors.grey.shade400,
                          ),
                        );
                      }),
                    ),
                    const SizedBox(height: 8),
                    Stack(
                      children: [
                        Container(
                          height: 6,
                          width: double.infinity,
                          decoration: BoxDecoration(
                            color: Colors.grey.shade200,
                            borderRadius: BorderRadius.circular(3),
                          ),
                        ),
                        AnimatedContainer(
                          duration: const Duration(milliseconds: 450),
                          height: 6,
                          width: MediaQuery.of(context).size.width *
                              (0.1 + 0.4 * _currentStep),
                          decoration: BoxDecoration(
                            gradient: const LinearGradient(
                              colors: [Color(0xFF00ACC1), Color(0xFF006A7A)],
                            ),
                            borderRadius: BorderRadius.circular(3),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              
              // Header text
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 32.0),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        stepTitles[_currentStep],
                        style: const TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF004D5A),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        stepSubtitles[_currentStep],
                        style: const TextStyle(
                          fontSize: 14,
                          color: Color(0xFF6B8B88),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Page Form Content
              Expanded(
                child: PageView(
                  controller: _pageController,
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    _buildStep1(),
                    _buildStep2(),
                    _buildStep3(),
                  ],
                ),
              ),

              // Footer Buttons
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    if (_currentStep > 0)
                      TextButton(
                        onPressed: _prevPage,
                        child: const Text(
                          "BACK",
                          style: TextStyle(
                            color: Color(0xFF007A87),
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1,
                          ),
                        ),
                      )
                    else
                      const SizedBox(width: 80),
                    
                    GlowingButton(
                      onTap: _nextPage,
                      child: Text(
                        _currentStep == 2 ? "NAVIGATE TO FLOW" : "NEXT STEP",
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // STEP 1: Personal Info
  Widget _buildStep1() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 8.0),
      child: Column(
        children: [
          const SizedBox(height: 8),
          _buildTextField("First Name", _firstNameCtrl, Icons.person_outline),
          const SizedBox(height: 20),
          _buildTextField("Last Name", _lastNameCtrl, Icons.person_outline),
          const SizedBox(height: 20),
          _buildTextField("Student Roll Number / ID", _rollNoCtrl, Icons.badge_outlined),
          const SizedBox(height: 40),
          // Flow message
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.teal.shade50.withOpacity(0.4),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.teal.shade100, width: 1),
            ),
            child: Row(
              children: [
                const Icon(Icons.info_outline, color: Color(0xFF007A87), size: 24),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    "Your placement profile directs custom career recommendations and mock test materials.",
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.teal.shade900,
                      height: 1.4,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // STEP 2: Academic Info
  Widget _buildStep2() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildTextField("College / Institution", _collegeCtrl, Icons.school_outlined),
          const SizedBox(height: 20),
          _buildTextField("Department / Branch", _departmentCtrl, Icons.account_tree_outlined),
          const SizedBox(height: 20),
          _buildTextField("Current GPA / CGPA", _gpaCtrl, Icons.grade_outlined, keyboardType: TextInputType.number),
          const SizedBox(height: 24),
          const Text(
            "Current Academic Year",
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Color(0xFF004D5A),
            ),
          ),
          const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: List.generate(4, (idx) {
              final year = idx + 1;
              final isSelected = _selectedYear == year;
              return Expanded(
                child: GestureDetector(
                  onTap: () {
                    setState(() {
                      _selectedYear = year;
                    });
                  },
                  child: Container(
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    decoration: BoxDecoration(
                      color: isSelected ? const Color(0xFF007A87) : Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: isSelected ? Colors.transparent : Colors.grey.shade300,
                        width: 1.5,
                      ),
                      boxShadow: isSelected
                          ? [BoxShadow(color: const Color(0xFF007A87).withOpacity(0.3), blurRadius: 6, offset: const Offset(0, 3))]
                          : null,
                    ),
                    child: Center(
                      child: Text(
                        "Year $year",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: isSelected ? Colors.white : Colors.grey.shade700,
                          fontSize: 13,
                        ),
                      ),
                    ),
                  ),
                ),
              );
            }),
          ),
        ],
      ),
    );
  }

  // STEP 3: Skills & Targets
  Widget _buildStep3() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Target Roles Inputs
          const Text(
            "Target Placement Roles",
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Color(0xFF004D5A),
            ),
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _rolesCtrl,
                  decoration: _inputDecoration("Add target role (e.g. SDE, Data Analyst)", Icons.work_outline),
                  onSubmitted: (_) => _addRole(),
                ),
              ),
              const SizedBox(width: 8),
              IconButton(
                icon: const Icon(Icons.add_circle, color: Color(0xFF00ACC1), size: 32),
                onPressed: _addRole,
              ),
            ],
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8.0,
            children: _rolesList.map((role) {
              return Chip(
                label: Text(role),
                backgroundColor: const Color(0xFFE0F2F1),
                deleteIconColor: const Color(0xFF00796B),
                onDeleted: () {
                  setState(() {
                    _rolesList.remove(role);
                  });
                },
              );
            }).toList(),
          ),
          
          const SizedBox(height: 24),
          
          // Skills Inputs
          const Text(
            "Top Skills",
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Color(0xFF004D5A),
            ),
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _skillsCtrl,
                  decoration: _inputDecoration("Add skill (e.g. Flutter, FastAPI, Python)", Icons.bolt_outlined),
                  onSubmitted: (_) => _addSkill(),
                ),
              ),
              const SizedBox(width: 8),
              IconButton(
                icon: const Icon(Icons.add_circle, color: Color(0xFF00ACC1), size: 32),
                onPressed: _addSkill,
              ),
            ],
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8.0,
            children: _skillsList.map((skill) {
              return Chip(
                label: Text(skill),
                backgroundColor: const Color(0xFFE0F7FA),
                deleteIconColor: const Color(0xFF00838F),
                onDeleted: () {
                  setState(() {
                    _skillsList.remove(skill);
                  });
                },
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller, IconData icon, {TextInputType keyboardType = TextInputType.text}) {
    return TextField(
      controller: controller,
      keyboardType: keyboardType,
      decoration: _inputDecoration(label, icon),
    );
  }

  InputDecoration _inputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Color(0xFF6B8B88), fontSize: 13),
      prefixIcon: Icon(icon, color: const Color(0xFF007A87)),
      filled: true,
      fillColor: Colors.white,
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(16),
        borderSide: BorderSide(color: Colors.grey.shade300),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(16),
        borderSide: const BorderSide(color: Color(0xFF007A87), width: 1.5),
      ),
    );
  }
}
