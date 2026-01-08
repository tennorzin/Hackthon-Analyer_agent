from analyzer_agent.analyzer_tool import analyze_sow_with_rag

# Read SOW text
with open("analyzer_agent/test_input.txt", "r", encoding="utf-8") as f:
    sow_text = f.read()

# Run Analyzer Tool
result = analyze_sow_with_rag(sow_text)

print("\n=== Analyzer Tool Output ===\n")
print(result)
