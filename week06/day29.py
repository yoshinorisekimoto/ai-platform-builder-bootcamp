evidence = """
Sales: $4M expansion. Contract must be signed this quarter.
Sales: The contract can be signed this quarter even if the launch happens later.
Engineering: 9-week target with 70% confidence.
Dependency: Authentication upgrade.
Product: Prefers a global standard solution.
Partner: Accepts a 9-week launch timeline.
Engineering: If the dependency is resolved by Week 6, confidence increases to 90%.

"""

print(evidence)

prompt = f"""

You are supporting a senior Platform Partnerships leader.

Organize the following evidence into an executive decision brief.

Do NOT make the final decision.
Do not invent facts that are not in the evidence.
Clearly label any inference or assumption.
If evidence is missing, say "Insufficient evidence".
Separate facts from hypotheses.
Do not propose new solution options unless they are directly supported by the evidence. Put speculative ideas under "Hypotheses to Validate".
Preserve commercial conditions exactly as stated. Do not replace "contract signature", "launch", "delivery", or "revenue recognition" with one another.

Return:
1. Key Evidence
2. Stakeholder Concerns
3. Unresolved Questions
4. Options and Trade-offs
5. Risks

Evidence:
{evidence}
"""

print(prompt)

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input=prompt
)

print("\n--- AI Decision Brief ---")
print(response.output_text)