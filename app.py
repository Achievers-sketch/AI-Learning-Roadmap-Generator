import os
import gradio as gr
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def generate_roadmap(
    domain,
    level,
    duration,
    hours_per_week,
    goal
):

    if not domain.strip():
        return "⚠️ Please enter a learning domain."

    if not goal.strip():
        goal = "Develop strong practical skills in this field."

    prompt = f"""
You are an expert learning curriculum designer.

Create a personalized learning roadmap.

Learner profile:

Domain:
{domain}

Skill level:
{level}

Learning duration:
{duration}

Available study time:
{hours_per_week} hours per week

Learning goal:
{goal}

Create a realistic and practical learning roadmap.

Include:

# Learning Roadmap

## Learning Goal

## Prerequisites

## Roadmap Overview

## Phase-by-Phase Roadmap

For each phase include:
- Topics
- Concepts
- Practical exercises
- Expected outcome

## Weekly Schedule

For each week include:
- Topics
- Practice
- Project/task
- Expected outcome

## Practical Projects

## Recommended Resources

## Milestones

## Final Capstone Project

## Expected Skills

Make the roadmap realistic for the learner's
available time and current skill level.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert learning "
                        "curriculum designer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"❌ Error: {str(e)}"


with gr.Blocks(
    title="AI Learning Roadmap Generator"
) as demo:

    gr.Markdown(
        """
        # 🧠 AI Learning Roadmap Generator

        Create a personalized learning roadmap
        for any field.
        """
    )

    domain = gr.Textbox(
        label="📚 Learning Domain",
        placeholder="e.g. Python, AI, Biomedical Engineering"
    )

    level = gr.Dropdown(
        choices=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value="Beginner",
        label="📊 Skill Level"
    )

    duration = gr.Dropdown(
        choices=[
            "4 weeks",
            "8 weeks",
            "12 weeks",
            "16 weeks",
            "6 months",
            "1 year"
        ],
        value="12 weeks",
        label="⏱️ Learning Duration"
    )

    hours = gr.Slider(
        minimum=1,
        maximum=40,
        value=8,
        step=1,
        label="⏰ Hours Per Week"
    )

    goal = gr.Textbox(
        label="🎯 Learning Goal",
        placeholder="e.g. Become job-ready"
    )

    generate_button = gr.Button(
        "🚀 Generate Roadmap",
        variant="primary"
    )

    output = gr.Markdown(
        label="Your Roadmap"
    )

    generate_button.click(
        fn=generate_roadmap,
        inputs=[
            domain,
            level,
            duration,
            hours,
            goal
        ],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch()
