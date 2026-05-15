# GitHub Copilot Intermediate Lab Instructions
**Duration:** 2 hours  
**Level:** Intermediate

---

## Pre-Lab Setup (15 minutes before lab)

### 1. Prerequisites
- GitHub Copilot license activated
- VS Code with GitHub Copilot extensions installed
- Python 3.9+ installed
- Git configured

### 2. Clone and Env Setup
- Clone this repository
- Run in terminal:
```bash
cd steel-inventory-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Verify Setup
```bash
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs - you should see the API documentation.

### 4. Initial Commit
```bash
git init
git add .
git commit -m "Initial project scaffold"
git branch -M main
```

---

## Lab Overview

You'll enhance a partially implemented Steel Inventory Management API using GitHub Copilot's advanced features. The starter code has intentional bugs, missing features, and incomplete tests.

### Learning Objectives Checklist
- [ ] Apply decomposition prompting
- [ ] Use test-first development
- [ ] Apply refactor-first patterns
- [ ] Generate PR summaries
- [ ] Generate semantic commit messages
- [ ] Perform Copilot code reviews (multiple modes)
- [ ] Create custom agents (.agent.md)
- [ ] Create agent skills (SKILL.md)
- [ ] Use Copilot Memory

---

## Part 1: Advanced Prompting Patterns (35 minutes)

### Exercise 1.1: Discover and Fix Bugs Using Copilot (15 min)

**Task:** Use Copilot to find bugs, then fix them with decomposition prompting

#### Step 1: Bug Discovery (5 min)

Use Copilot's review capabilities to discover issues in the codebase:

1. **Workspace-wide review:**
   Open Copilot Chat and drag the steel-inventory-api folder into the chat as context, then type:

   ```
   Review the application for any issues
   ```
   Review the suggestions and note any critical issues found. You should discover at least 3-5 issues.
   
   > Note: We added the steel-inventory-api to the context in order for Copilot to not read the LAB_INSTRUCTIONS.md file and flag it as a bug. This way, we can focus on the actual code files.

2. **Targeted file analysis:**
   For each key file, ask Copilot to analyze for common issues:
   ```
   Review database.py for potential bugs including:
   - Data validation issues
   - Missing error handling
   - State management problems
   ```
   
   ```
   Review routers/inventory.py for:
   - Input validation issues
   - Missing boundary checks
   - Error handling gaps
   ```
   
   ```
   Review steel_utils.py for:
   - Null/None handling issues
   - Type safety problems
   - Edge cases not handled
   ```

3. **Document your findings:**
   As Copilot identifies issues, note them down. You should discover bugs like:
   - Duplicate product codes not prevented
   - `last_updated` not set on updates
   - Negative quantities allowed
   - Crashes on None/null values

#### Step 2: Fix Bugs Using Decomposition (10 min)

Now fix the bugs you discovered using decomposition prompting. For this step, we will focus on 3 critical bugs. 
- Duplicate product codes not prevented in database.py
- No Negative Quantity Validation in routers/inventory.py
- Null Pointer in calculate_area_m2() for steel_utils.py

1. For each bug found, use this sample decomposition pattern in Copilot Chat:
   ```
   I need to fix the [bug description] in [file name]. Let's break this down:
   1. First, show me where [relevant code section]
   2. Then, suggest [solution approach]
   3. Finally, show where to add this [implementation]
   ```

2. Example for duplicate product code bug in database.py:
   ```
   I need to fix the duplicate product code bug in database.py. Let's break this down:
   1. First, show me where product codes are validated
   2. Then, suggest validation logic to check for duplicates
   3. Finally, show where to add this validation in the create method
   ```
   Open the relevant file, review the suggested validation logic, and implement it with Copilot's help.

3. Fix the other bugs using decomposition:
   - No Negative Quantity Validation in routers/inventory.py
   - Null Pointer in calculate_area_m2() for steel_utils.py

   For each bug, use decomposition:
   - Identify the problem location (already done in Step 1)
   - Understand the root cause
   - Propose a solution
   - Implement with Copilot's help

   Use the sample decomposition prompt for each bug.

**Expected Outcome:** 
- You've practiced using Copilot for code discovery at multiple levels
- All discovered bugs are fixed with clear, maintainable code
- You understand finding AND fixing issues with Copilot
- You've identified architectural improvements

**Commit:** 
Go to Source Control and use Copilot to generate a semantic commit message for your changes. Then Commit & Push your changes.

---

### Exercise 1.2: Test-First Development (10 min)

**Task:** Add comprehensive tests BEFORE implementing new features

1. Open `tests/test_inventory.py`. Close any other files to focus on testing.
2. In Copilot Chat, use test-first prompting:
```
Using TDD, I want to add a feature to search products by grade. 
First, write comprehensive tests for this feature including:
- Searching for existing grade
- Searching for non-existent grade
- Case-insensitive search
- Empty results handling

Don't implement the feature yet, just the tests.
```

3. Run the tests (they should fail):
```bash
pytest tests/test_inventory.py -v
```

4. Now ask Copilot to implement the feature to make tests pass:
```
Now implement the search_by_grade endpoint in routers/inventory.py to make these tests pass
```
5. Review the implementation, run tests again, and ensure they pass.

**Expected Outcome:** 
- Tests written first (failing)
- Feature implemented (tests passing)

**Commit:**
Go to Source Control and use Copilot to generate a semantic commit message for your changes. Then Commit & Push your changes.

---

### Exercise 1.3: Refactor-First Pattern (10 min)

**Task:** Refactor the steel_utils.py before adding new features

1. Open `app/utils/steel_utils.py`
2. Use refactor-first prompting:
```
I want to add weight calculations for coil, bar, and tube shapes.
Before adding new features, let's refactor the existing code:
1. Extract shape-specific calculations into separate functions
2. Add proper type hints
3. Add comprehensive docstrings
4. Add input validation

Show me the refactored structure first.
```

3. Review the refactoring suggestions
4. Apply the refactoring
5. NOW add the new calculations:
```
Now implement weight calculations for:
- coil (use rectangular approximation)
- bar (circular cross-section: π * r² * length * density)
- tube (hollow circular: π * (r_outer² - r_inner²) * length * density)
```

**Expected Outcome:**
- Clean, well-structured code
- All shape types supported
- Proper documentation

**Commit:**
Go to Source Control and use Copilot to generate a semantic commit message for your changes. Then Commit & Push your changes.

---

## Part 2: GitHub Workflow Integration (15 minutes)

### Exercise 2.1: Create Feature Branch with PR (10 min)

1. Create a new feature branch:
```bash
git checkout -b feature/low-stock-alerts
```

2. Implement low stock alert feature. Ask Copilot:
```
Add a low stock alert feature:
1. Add a `min_stock_level` field to SteelProduct model
2. Create an endpoint GET /inventory/low-stock that returns products below their minimum
3. Add a field to track whether an alert has been sent
```
Implement the feature with Copilot's help.

---
### Exercise 2.2: Generate Commit Message (10 min)

1. Go to Settings and search for "Commit Message Instructions". 

2. Select "Edit settings in json".

3. In the settings file enter the following:
```json
"github.copilot.chat.commitMessageGeneration.instructions": [
   {
      "file": ".github/instructions/.copilot-commit-message-instructions.md"
   }
]
```
   Save the file.

4. Create an instructions directory in the .github folder if it doesn't exist and add a file called `.copilot-commit-message-instructions.md` with the following content:

```markdown
# Commit Message Guidelines

Write clear, concise commit messages using this format:

## Format
<type>: <short summary>

**Limit to 50 characters** when possible. Use present tense ("Add feature" not "Added feature").

## Common Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **refactor**: Code restructuring
- **test**: Test additions or updates
- **chore**: Maintenance tasks

## Optional Details
Add a blank line and longer description if needed:
- Explain **why** the change was made
- Reference issues: `Fixes #123` or `Closes #456`
- Note breaking changes: `BREAKING CHANGE: description`

## Examples
feat: Add inventory search endpoint
fix: Resolve null pointer in steel calculator
docs: Update API usage examples

```
   Save the file.

5. Go to Source Control and use Copilot to generate a semantic commit message for your changes. Verify that it uses the guidelines you just set and edit if necessary to ensure it accurately reflects your changes.

6. Then Commit & Push your changes.

---
### Exercise 2.3: Generate PR Summary (5 min)

1. Create a Pull Request for your feature branch against main. Go to your GitHub repository and you should see a Compare & Pull Request button. Click it.

2. Go to the description box of the PR and remove any auto-generated text.

3. Search for the Copilot Icon in the description box and click Generate -> Summary to generate a PR summary.

4. Review the generated summary and make any necessary edits to ensure it accurately reflects the changes made in the PR.

5. Click Create Pull Request to submit your PR with the generated summary.

> Note: In the advanced course, we will use GitHub MCP Server to automate PR summary generation.
---

## Part 3: Custom Agents and Skills (40 minutes)

**Setup:** Switch back to the main branch before starting this section:
```bash
git checkout main
```

This ensures your custom agents and skills are available across all future branches.

---

### Exercise 3.1: Create Custom Agent (20 min)

**Task:** Create specialized agents for steel calculations from scratch using either the /create-agent command or manual creation.

1. Create **steel-expert.agent.md** in `.github/agents/` using /create-agent command:

Ask Copilot in **Agent** mode to help you structure it:
```
/create-agent I want to create a custom GitHub Copilot agent for steel manufacturing expertise.
Create an agent file called steel-expert.agent.md that:
- Specializes in steel grades, calculations, and specifications
- Has access to read and web tools
- Knows about ASTM and EN standards
- Can perform weight and dimension calculations
- Uses Claude Sonnet 4.5 model
```
Verify the generated agent file in the **.github/agents directory**. If the file is generated elsewhere (e.g., project root), move it to: 
.github/agents/steel-expert.agent.md

It should have proper YAML frontmatter and a detailed description of the agent's capabilities similar to below:
```
name: steel-expert
description: "Steel manufacturing specialist. Use when: calculating steel weight, dimensions, or area; identifying steel grades; interpreting ASTM or EN standards; providing material specifications; performing metallurgical calculations; advising on steel properties"
tools: [read, web]
model: "Claude Sonnet 4.5"
argument-hint: "Ask about steel grades, calculations, or standards"
```

Review the following key sections in the generated agent file:
- **Description**: Should clearly state the agent's expertise in steel manufacturing, including knowledge of steel grades, standards, and calculations.
- **Tools**: Should include `read` and `web` tools for accessing information.
- **Model**: Should specify `Claude Sonnet 4.5`
- **Role**: Should outline the agent's role in answering questions related to steel products, calculations, and standards.

2. **Test your steel-expert agent:**
- In Copilot Chat select the **steel-expert** agent and ask it a question:
```
What's the weight of a 304 stainless steel sheet 2400x1200x6mm?
```

3. **Create inventory-manager.agent.md** with handoffs using /create-agent command:

Go back to **Agent mode**. Ask Copilot:
```
/create-agent Create an inventory-manager.agent.md that:
- Manages inventory operations
- Delegates calculations to steel-expert agent using handoffs
- Has access to read and web tools
- Uses Claude Sonnet 4.5 model
```
Verify the generated agent file in the **.github/agents directory**. If the file is generated elsewhere, move it to the correct location.

Here is a sample structure for the inventory-manager agent with handoffs to steel-expert:
```
name: inventory-manager
description: "Inventory operations manager. Use when: managing steel inventory; adding or updating products; checking stock levels; organizing warehouse locations; tracking inventory movements; coordinating product data"
tools: [read, web, agent]
model: "Claude Sonnet 4.5"
argument-hint: "Describe inventory operation or product management task"
handoffs:
  - label: Send to steel expert
    agent: steel-expert
    prompt: Implement the needed computation
    send: true
```
> Note how the handoff is structured with a label, target agent, prompt, and send flag. The /create-agent command may not generate the handoff section correctly, so you may need to add it manually as shown above.

Review the following key sections in the generated agent file:
- **Description**: Should clearly state the agent's role in managing inventory operations, including delegating calculations to the steel-expert agent using handoffs. It should specify that this agent is responsible for inventory management tasks and will rely on the steel-expert for any calculations related to steel products.
- **Tools**: Should include `read` and `web` tools for accessing information.
- **Model**: Should specify `Claude Sonnet 4.5`
- **Handoffs**: Should include a handoff to the steel-expert agent for any calculations or technical questions related to steel products.
- **Role**: Should outline the agent's role in managing inventory operations and coordinating with the steel-expert agent for calculations.

4. **Test handoff between agents:**

Select the **inventory-manager** agent in Copilot Chat and ask it a question that requires a handoff:
```
Given this: A36 plate, 3000x1500x10mm, qty 50. 
What's its weight?
```

5. **Create quality-inspector.agent.md** manually for quality control:
```markdown
---
name: quality-inspector
description: Inspects steel products for defects and compliance
tools:
  - read
  - web
model: Claude Sonnet 4.5
---

You are a quality control specialist for steel manufacturing.

Your responsibilities:
- Inspect products for dimensional accuracy
- Verify material properties
- Check compliance with specifications
- Recommend corrective actions

Use precise measurements and cite quality standards (ASTM, ISO).
```

6. Select the **quality-inspector** agent in Copilot Chat and Test your new agent:
```
Check if a steel sheet with thickness 5.8mm meets the specification of 6mm ±0.3mm
```

7. Test **user-invocable** setting for steel-expert.

Go to the steel-expert.agent.md file and add `user-invocable: false` to the YAML frontmatter and save the file. Then try to invoke the steel-expert agent directly in Copilot Chat.

Example:
```
name: steel-expert
description: "Steel manufacturing specialist. Use when: calculating steel weight, dimensions, or area; identifying steel grades; interpreting ASTM or EN standards; providing material specifications; performing metallurgical calculations; advising on steel properties"
tools: [read, web]
model: "Claude Sonnet 4.5"
argument-hint: "Ask about steel grades, calculations, or standards"
user-invocable: false
```

Verify that the steel-expert agent is no longer available for direct invocation.
You should not see "steel-expert" in the agent selector dropdown in Copilot Chat.

8. Go to the inventory-manager agent and test that the handoff to steel-expert still works even after setting it to non-user-invocable:

Select the **inventory-manager** agent in Copilot Chat and ask it a question that requires a handoff:
```
Given this: A36 plate, 3000x1500x10mm, qty 50. 
What's its weight?
```

**Expected Outcome:**
- Custom agents responding appropriately
- Handoff working between agents
- Specialized responses based on agent context

---

### Exercise 3.2: Create Agent Skills (20 min)

**Task:** Create portable skills following the agentskills.io standard from scratch using either the /create-skill command or manual creation.

1. Create **cost-estimation.skill** in `skills/cost-estimation/SKILL.md` using /create-skill command:

Ask Copilot:
```
/create-skill I want to create an agent skill following the agentskills.io standard.
Create a SKILL.md file for cost-estimation that:
- Has proper YAML frontmatter (name, description, author, version, agentSkillsVersion: 0.1.0)
- Calculates material costs, shipping expenses, and project estimates
- Includes formulas for material cost, shipping cost, and total cost
- Supports different pricing scenarios
- Includes usage examples with cost calculations
```
Things to verify:
- SKILL.md file is created in the correct location: `skills/cost-estimation/SKILL.md`
- YAML frontmatter is properly formatted and must have the following fields at minimum:
   - **Name**: Should be `cost-estimation` (must match the directory name)
   - **Description**: Should clearly explain that this skill calculates material costs, shipping expenses, and project estimates for steel products.

2. **Test the cost-estimation skill:**

Open a new Copilot Chat, select the **Agent** mode and ask it to use the cost-estimation skill:
```
Use the cost-estimation skill to estimate total cost:
Product: A36 plate 3000x1500x10mm
Quantity: 50 units
Unit weight: 353.25 kg
Steel price: $0.85/kg
Shipping distance: 500 km at $0.12/kg/100km
```

3. Create **inventory-optimization.skill** in `skills/inventory-optimization/SKILL.md` manually.

Create a directory called `inventory-optimization` under `skills/` and add a `SKILL.md` file with the following content:

```markdown
---
name: inventory-optimization
description: Optimize inventory levels and reorder points
---

# Inventory Optimization Skill

Provides recommendations for optimal inventory management.

## Capabilities

- Calculate reorder points
- Suggest optimal stock levels
- Identify slow-moving inventory
- Forecast demand

## Usage

Invoke when:
- Planning inventory levels
- Analyzing stock turnover
- Optimizing warehouse space

## Examples
Calculate reorder point for:
- Product: STL-001
- Lead time: 7 days
- Daily usage: 5 units
- Safety stock: 20 units

## Formula
Reorder Point = (Lead Time × Daily Usage) + Safety Stock
```

4. **Test the new skill:**
```
Use the inventory-optimization skill to calculate reorder point:
lead time 7 days, daily usage 10 units, safety stock 50 units
```

5. Add progressive loading to your skills. Modify the computation of the inventory-optimization skill to load seasonality data from a file before performing the calculation. 

Modify the later part of the SKILL.md file:

```
## Formula
Reorder Point = (Lead Time × Daily Usage) * Seasonality Factor + Safety Stock

Determine the Seasonality Factor based on the current month using the seasonality rules defined in `seasonality.md`.
```

Then create a `seasonality.md` file in the same directory with the following content:

```markdown
If December: Seasonality Factor = 1.2
Otherwise: Seasonality Factor = 1.0
```
6. Test that the inventory-optimization skill correctly applies the seasonality factor based on the current month when calculating the reorder point.
Create a new Copilot Chat and ask:
```
Use the inventory-optimization skill to calculate reorder point:
lead time 7 days, daily usage 10 units, safety stock 50 units in December
```

**Expected Outcome:**
- Skill properly structured
- Progressive loading working

---

## Part 4: Copilot Memory (10 minutes)

### Exercise 4.1: Use Copilot Memory (10 min)

**Task:** Store and retrieve BlueScope-specific standards

1. Enable Copilot Memory in VS Code settings if not already enabled.
- Select the settings icon in the bottom left corner of VS Code
- Search for "Copilot Memory"
- Enable the feature for both Tools and Chat and save settings

2. Open Copilot Chat and teach it BlueScope standards:
```
Remember: BlueScope uses the following standard locations:
- Warehouse-A: Hot-rolled products
- Warehouse-B: Cold-rolled and coated products
- Warehouse-C: Long products (bars, tubes)

Remember: Minimum stock levels by shape:
- Sheets: 100 units
- Coils: 50 units
- Plates: 75 units
- Bars: 200 units
- Tubes: 150 units

Remember: Our quality grades:
- Premium: aerospace, automotive
- Standard: construction, general manufacturing
- Economy: non-critical applications

Put these in repository memory.
```
Verify that a memory file is created.

3. Test memory recall. Open a new chat and ask:
```
What's the standard minimum stock level for sheets?
```

```
Where should I store hot-rolled coils?
```

4. Use memory in code generation:
```
Update the SteelProduct model to include quality_grade and set appropriate defaults based on what you remember
```

5. View your repository memory:
- Go to your repository on GitHub
- Click on Settings → Copilot → Memory
- Review the stored memories and their details
- You may also delete memories from this view if needed

**Expected Outcome:**
- Copilot recalls BlueScope-specific information
- Suggestions align with stored preferences
- Memory persists across chat sessions

---

## Final Challenge: Build a Plan/Implement/Review Pipeline (15 minutes)

**Goal:** Create a complete coil quality grading feature using a structured Plan → Implement → Review workflow with a supporting skill.

### Context

BlueScope needs to implement an automated quality grading system for steel coils. The system must evaluate coils based on surface defects, dimensional accuracy, and coating uniformity, then assign a quality grade (Premium, Standard, or Economy).

### Task Overview

You will:
1. **Plan** the feature architecture and requirements
2. Create a **quality-grading skill** to encapsulate grading logic
3. **Implement** the quality grading endpoint and model changes
4. **Review** the implementation using Copilot's review capabilities
5. Test the complete workflow with your custom agents

---

### Step 1: Plan Phase (5 min)

Use decomposition prompting to plan the feature architecture:

1. Open a new Copilot Chat and ask:
```
I need to implement a coil quality grading feature for BlueScope's steel inventory API.
Let's plan this systematically:

1. First, what data fields do we need to track quality metrics for coils?
   Consider: surface defects, dimensional accuracy, coating uniformity

2. Then, what business logic determines the grade assignment?
   Use the grades from memory: Premium, Standard, Economy

3. Finally, what API endpoints and model changes are needed?
   Consider: grading endpoint, model updates, validation

Provide a structured plan with specific requirements for each component.
```

2. Review Copilot's plan and refine it by asking follow-up questions:
```
What validation rules should we apply to ensure data quality?
```

```
Should the grading be calculated automatically or manually triggered?
```

3. Document the plan for future reference and implementation guidance:
```
Save the complete plan in a markdown file called `coil-quality-grading-plan.md` in the project root.
```

**Expected Outcome:**
- Clear architectural plan documented
- Requirements broken down into implementable tasks
- Understanding of data flow and business logic

---

### Step 2: Create Quality Grading Skill (3 min)

Before implementing, create a reusable skill for the grading logic:

1. Ask Copilot:
```
/create-skill Create a quality-grading.skill in skills/quality-grading/SKILL.md that:
- Has proper YAML frontmatter (name: quality-grading, description)
- Defines grading criteria for steel coils based on:
  * Surface defect score (0-100, higher is better)
  * Dimensional accuracy percentage (0-100%)
  * Coating uniformity score (0-100)
- Includes grading rules:
  * Premium: All scores ≥ 95
  * Standard: All scores ≥ 80 and < 95
  * Economy: Any score < 80
- Provides usage examples for calculating grades
```

2. Verify the generated SKILL.md file in `skills/quality-grading/` directory (move it if needed)

3. Ensure the YAML frontmatter includes at minimum:
   - name: quality-grading
   - description: Clear explanation of coil quality grading

4. Test the skill immediately:
```
Use the quality-grading skill to determine the grade for a coil with:
- Surface defect score: 96
- Dimensional accuracy: 98%
- Coating uniformity: 97
```

**Expected Outcome:**
- Reusable skill created following agentskills.io standard
- Grading logic clearly documented
- Skill responds correctly to test scenarios

---

### Step 3: Implement Phase (4 min)

Implement the feature using test-first development:

1. **Write tests first** - In Copilot Chat:
```
Using TDD, create comprehensive tests in tests/test_inventory.py for coil quality grading

Use the tests documented in coil-quality-grading-plan.md as a reference.

Use the quality-grading skill's rules for grade assignment logic.
```

2. **Update the model** - Ask Copilot:
```
Add quality metrics fields to the SteelProduct model in models.py:
- surface_defect_score: float (0-100)
- dimensional_accuracy: float (0-100)
- coating_uniformity: float (0-100)
- quality_grade: str (auto-calculated based on scores)

Include validation to ensure scores are within 0-100 range.
```

3. **Create the grading endpoint** - Ask Copilot:
```
Create a POST endpoint /inventory/{product_id}/grade in routers/inventory.py that:
- Accepts quality metrics (surface_defect_score, dimensional_accuracy, coating_uniformity)
- Calculates quality_grade using the quality-grading skill rules
- Updates the product record
- Returns the updated product with assigned grade

Use proper error handling for invalid product codes and out-of-range scores.
```

4. **Run tests in terminal**:
```bash
pytest tests/test_inventory.py -v
```

You may also ask Copilot test the changes done:
```
Test the coil quality grading implementation using test_inventory.py to ensure all tests pass and the grading logic is correct. Activate the environment first before running the tests.
```

**Expected Outcome:**
- Tests written and passing
- Model updated with quality fields
- API endpoint functional
- Validation working correctly

---

### Step 4: Review Phase (2 min)

Use Copilot's review capabilities to validate your implementation:

1. **Comprehensive code review** - Open Copilot Chat and ask:
```
Review the coil quality grading implementation for:
- Code quality and best practices
- Potential bugs or edge cases
- Security considerations (input validation)
- Performance implications
- Documentation completeness

Focus on routers/inventory.py, models.py, and tests/test_inventory.py
```

2. **Review specific concerns**:
```
Are there any edge cases in the grading logic that aren't covered by tests?
```

```
Is the validation robust enough to prevent invalid data from being stored?
```

3. **Address any issues** found by Copilot using decomposition:
```
For the [issue found], let's fix it step by step:
1. First, explain why this is a problem
2. Then, suggest the best solution approach
3. Finally, show the implementation
```
> Note: You may skip this in the interest of time, but in a real scenario, you would want to address any critical issues found during the review.

**Expected Outcome:**
- Code reviewed and any issues identified
- Edge cases discovered and addressed
- Implementation validated against requirements

---

### Step 5: Integration Test with Custom Agents (1 min)

Test the complete workflow using your custom agents:

1. **Test with quality-inspector agent:**

Select the **quality-inspector** agent and ask:
```
Inspect this coil quality data and recommend a grade:
- Surface defect score: 92
- Dimensional accuracy: 88%
- Coating uniformity: 91

Does this meet our quality standards?
```

2. **Test with inventory-manager agent:**

Select the **inventory-manager** agent and ask:
```
Add a new coil to inventory:
- Product code: COIL-QA-001
- Shape: coil
- Grade: A36
- Location: Warehouse-B
Then grade it with: surface_defect_score=96, dimensional_accuracy=98, coating_uniformity=97
```

**Expected Outcome:**
- Agents correctly handle quality grading context
- Integration works end-to-end
- Agents leverage the quality-grading skill appropriately

---

### Deliverables

- ✅ Documented implementation plan
- ✅ quality-grading.skill created and tested
- ✅ Tests written (TDD approach)
- ✅ Model updated with quality fields
- ✅ Grading endpoint implemented
- ✅ Code reviewed and validated
- ✅ Integration tested with custom agents
- ✅ All tests passing

**Commit your final work:**
Go to Source Control and use Copilot to generate a semantic commit message for your complete quality grading implementation. Commit & Push your changes.

---

## Lab Completion Checklist

### Skills Demonstrated
- [x] Decomposition prompting
- [x] Test-first development
- [x] Refactor-first patterns
- [x] Multi-turn refinement
- [x] PR summary generation
- [x] Semantic commit messages
- [x] Copilot code review (bug discovery + comprehensive review modes)
- [x] Custom agent creation (.agent.md)
- [x] Agent skills (SKILL.md)
- [x] Copilot Memory
- [x] Diagnostics verification

### Deliverables
1. ✅ Discovered and fixed all bugs using Copilot review
2. ✅ Added grade search feature (TDD)
3. ✅ Completed weight calculations for all shapes
4. ✅ Implemented low stock alerts
5. ✅ Tested steel-expert and inventory-manager agents
6. ✅ Created custom quality-inspector agent
7. ✅ Created cost-estimation skill
8. ✅ Configured Copilot Memory with standards

---

