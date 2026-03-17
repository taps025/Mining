import base64
import html
import textwrap
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Mining War Room Presentation", layout="wide")

SECTIONS = [
    {
        "id": "engagement",
        "title": "Client Engagement:\nGreet & Meet\nSessions",
        "summary": "Client engagement strategy, current status, client service plan, and action priorities.",
        "content": [
            ("Strategic Objectives", [
                "Alignment: ensure services remain relevant to client operational needs.",
                "Retention: reinforce our value proposition.",
                "Growth: identify untapped opportunities where services can add value.",
            ]),
            ("Current Engagement Status", [
                "Initial Requests Sent: Completed (26 Feb 2026).",
                "Waiting for Response: Remaining clients - 13.",
                "Meeting scheduling and availability confirmation: High-priority clients and 4 clients to confirm their availability.",
            ]),
            ("Client Service Plan", [
                "Initial invitation sent to 17 clients.",
                "Follow-up to be done every 2 weeks.",
                "Confirm meeting dates once availability is received.",
                "Document action items and opportunities after each engagement.",
            ]),
            ("Action Plan", [
                "Implement a 14-day follow-up communication cycle.",
                "Conduct client follow-ups this week - completed on 10 March 2026.",
                "Confirm Greet & Meet session schedules once confirmations are received.",
                "Document engagement insights and opportunities.",
            ]),
        ],
    },
    {
        "id": "training",
        "title": "Intended\nUpcoming\nClient Trainings",
        "summary": "Training roadmap, target audience, and delivery formats for client capability-building in 2026.",
        "content": [
            ("Roadmap", [
                "This roadmap defines our educational framework for the 2026 fiscal year.",
                "By providing targeted training, we move beyond the role of a policy broker and become an integrated risk management partner.",
            ]),
            ("Objective", [
                "To empower client teams with the knowledge to reduce claims frequency and ensure regulatory compliance.",
            ]),
            ("Target Audience", [
                "HR Managers",
                "Operations Leads",
                "Safety Officers",
                "Staff",
                "Executives",
            ]),
            ("Delivery Formats", [
                "On-site workshops",
                "Quarterly webinars",
                "Online sessions",
            ]),
        ],
    },
    {
        "id": "pipeline",
        "title": "Active Leads\n& Pipelines",
        "summary": "Current live opportunities, owners, and pipeline movement.",
        "content": [
            ("Active Opportunities", [
                "Tataki Mining: work in progress - Tirelo.",
                "Lucara: engaging CEO and CFO - Tirelo.",
                "Maatla Resources: policy wording presentation in progress - Tshwarelo/Tirelo.",
                "Debswana Healthcare: healthcare solutions presented - Tirelo.",
                "Sandfire/Motheo Copper: awaiting introduction and engagement plan - Tirelo.",
            ]),
            ("Pipeline Notes", [
                "Power Plant Engineers: terms approved, awaiting KYC submission.",
                "Tau Freight Logistics: quotation shared, client reviewing and awaiting CEDA approval.",
                "Tardieu Botswana: client finalizing bank account for KYC submission.",
                "Mupane Gold Mining: matter before the Court of Appeal.",
            ]),
            ("Priority View", [
                "Focus on moving waiting items into submitted or invoiced stage.",
                "Resolve KYC and UBO blockers early to reduce slippage.",
                "Keep high-value accounts on structured follow-up cadence.",
            ]),
        ],
    },
]
SECTION_ORDER = [section["id"] for section in SECTIONS]


ENGAGEMENT_COLORS = ["#111111", "#c1121f", "#2b2b2b", "#e5383b"]
OUTREACH_STATUS = [
    {"Client": "Redpath", "Status": "Complete"},
    {"Client": "Okavango Diamond", "Status": "OK"},
    {"Client": "BotAsh", "Status": "Complete"},
    {"Client": "Letshego Africa", "Status": "Complete"},
    {"Client": "Air Liquide", "Status": "Take action urgently"},
    {"Client": "Botswana Oxygen", "Status": "Warning"},
    {"Client": "Final Energy Botswana", "Status": "OK"},
    {"Client": "Francistown Academic Hospital", "Status": "Take action urgently"},
    {"Client": "GH Group", "Status": "Warning"},
    {"Client": "Genesis HB Botswana", "Status": "Complete"},
    {"Client": "Mitchell Drilling Services", "Status": "Warning"},
    {"Client": "Minergy", "Status": "OK"},
    {"Client": "SDDS", "Status": "OK"},
    {"Client": "BG Motors", "Status": "Complete"},
]
ENGAGEMENT_ACTION_ITEMS = [
    "Implement a 14-day follow-up communication cycle.",
    "Conduct client follow-ups this week - completed on 10 March 2026.",
    "Confirm Greet & Meet session schedules once confirmations are received.",
    "Document engagement insights and opportunities.",
]
ENGAGEMENT_KEY_TARGET = (
    'Convert 60% of "Waiting for Response" leads into scheduled meetings by the end of March 2026.'
)
TRAINING_CONTINUATION_STEPS = [
    {
        "step": "Needs Assessment",
        "action": "Identify training gaps during training sessions.",
    },
    {
        "step": "Curriculum Design",
        "action": "Customize materials to client needs.",
    },
    {
        "step": "Delivery",
        "action": "Execute training on-site or virtually.",
    },
    {
        "step": "Verification",
        "action": "Evaluate effectiveness and learning outcomes.",
    },
]
PIPELINE_LEADS_TABLE = [
    {
        "client": "Tataki Mining",
        "income": "TBD",
        "comments": "Trying to find new contacts following a change in management from 2025.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Sesiro/Debswana Assets",
        "income": "TBD",
        "comments": "Minet to provide alternate solutions outside of the Anglo-Coromin arrangement.",
        "progress": "Quotes to be presented in March",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Lucara",
        "income": "TBD",
        "comments": "Engaging CEO and CFO.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Maatla Resources",
        "income": "TBD",
        "comments": "Lombard and BECI to present the policy wording to the Director of the Department of Mines for approval.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tshwarelo/Tirelo",
    },
    {
        "client": "Solex Power",
        "income": "TBD",
        "comments": "Looking to meet the project owners during the week starting 09/03.",
        "progress": "Set up another meeting",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Debswana Healthcare",
        "income": "TBD",
        "comments": "Healthcare solutions have been presented to the Debswana Wellness Fund.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Tardieu Botswana",
        "income": "TBD",
        "comments": "Client finalizing bank account setup for KYC submission.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tshwarelo/Tshenolo",
    },
    {
        "client": "Power Plant Engineers",
        "income": "TBD",
        "comments": "Terms approved and awaiting KYC submission to issue the invoices.",
        "progress": "Work in progress; UBO submission challenges",
        "estimated_placement": "TBD",
        "responsible_person": "Tshenolo",
    },
    {
        "client": "Tau Freight Logistics",
        "income": "TBD",
        "comments": "Quotation shared with the client and still under review. Client is waiting for approval from CEDA.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tshenolo",
    },
    {
        "client": "Sandfire/Motheo Copper",
        "income": "TBD",
        "comments": "Gross sell from GLA. Awaiting introduction, engagement dates, and plan.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Sesiro/JUP",
        "income": "TBD",
        "comments": "On track for August 2026.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
    {
        "client": "Mupane Gold Mining",
        "income": "TBD",
        "comments": "Before the Court of Appeal.",
        "progress": "Work in progress",
        "estimated_placement": "TBD",
        "responsible_person": "Tirelo",
    },
]


def get_pipeline_table() -> list[dict]:
    if "pipeline_table" not in st.session_state:
        st.session_state.pipeline_table = [row.copy() for row in PIPELINE_LEADS_TABLE]
    return st.session_state.pipeline_table


def load_image_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


LOGO_BASE64 = load_image_base64("logo.png") if Path("logo.png").exists() else ""


def render_html(html: str) -> None:
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


@st.dialog("Strategic Objectives")
def show_strategic_objectives_dialog() -> None:
    render_html(
        """
        <div class="objective-row top-row">
            <div class="objective-box narrow">
                <strong>Alignment:</strong><br>
                Ensure services remain relevant to the client's operational needs.
            </div>
            <div class="objective-box wide">
                <strong>Retention:</strong> Reinforce our value proposition.<br><br>
                <strong>How:</strong> Strengthen relationships through face-to-face or virtual interactions.
            </div>
            <div class="objective-box wide">
                <strong>Growth:</strong><br>
                Identify untapped opportunities where our services can add value.<br><br>
                <strong>How:</strong> Explore additional ways to support client operations and business growth.
            </div>
        </div>
        """
    )


@st.dialog("Current Engagement Status")
def show_status_dialog() -> None:
    render_html(
        """
        <div class="status-table-wrap">
            <div class="status-overview">
                <div class="status-chip complete">1 Completed</div>
                <div class="status-chip waiting">1 Waiting</div>
                <div class="status-chip progress">1 In Progress</div>
                <div class="status-bar">
                    <div class="status-bar-fill"></div>
                </div>
            </div>
            <table class="status-table-pretty">
                <thead>
                    <tr>
                        <th>Outreach Phase</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Initial Requests Sent</td>
                        <td>Completed (26 Feb 2026)</td>
                    </tr>
                    <tr>
                        <td>Waiting for Response</td>
                        <td>Remaining clients - 13</td>
                    </tr>
                    <tr>
                        <td>Meeting scheduling and availability confirmation</td>
                        <td>High-priority clients and 4 clients to confirm their availability</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    )


@st.dialog("Client Service Plan")
def show_approach_dialog() -> None:
    engagement_points = """
        <ul class="approach-bullets">
            <li>Re-discovery of the business</li>
            <li>Service review</li>
            <li>Claims</li>
            <li>Upselling</li>
            <li>Cross-selling</li>
        </ul>
    """
    steps = [
        ("01", "Outreach", "Initial invitation sent to 17 clients"),
        ("02", "Follow-Up", "To be done every 2 weeks"),
        ("03", "Meeting Confirmation", "Schedule meeting date"),
        (
            "04",
            "Engagement",
            engagement_points,
        ),
        ("05", "Action Plan", "Identify action items & opportunities"),
        ("06", "Destination", ""),
    ]

    for idx, (number, title, text) in enumerate(steps):
        left, middle, right = st.columns([0.12, 0.66, 0.22], gap="small")
        with left:
            render_html(f'<div class="approach-dot">{number}</div>')
        with middle:
            render_html(
                f"""
                <div class="approach-panel">
                    <div class="approach-heading">{title}</div>
                    <div class="approach-text">{text}</div>
                </div>
                """
            )
        with right:
            if idx == 0:
                with st.popover("View List", use_container_width=True):
                    st.markdown("**Initial invitation sent to 17 clients**")
                    st.table(OUTREACH_STATUS)
            else:
                st.empty()


@st.dialog("Action Plan")
def show_action_plan_dialog() -> None:
    action_items_html = "".join(
        f'<div class="action-plan-item"><div class="action-plan-dot"></div><div class="action-plan-copy">{html.escape(item)}</div></div>'
        for item in ENGAGEMENT_ACTION_ITEMS
    )

    render_html(
        f"""
        <style>
            .action-plan-stack {{
                display: grid;
                gap: 0.85rem;
                padding-top: 0.45rem;
            }}
            .action-plan-item {{
                display: grid;
                grid-template-columns: 16px 1fr;
                gap: 0.85rem;
                align-items: start;
                border-radius: 20px;
                padding: 1rem 1.05rem;
                background: linear-gradient(180deg, #ffffff 0%, #f7f7f7 100%);
                border: 1px solid rgba(17, 17, 17, 0.08);
                box-shadow: 0 14px 24px rgba(17, 17, 17, 0.05);
            }}
            .action-plan-dot {{
                width: 12px;
                height: 12px;
                border-radius: 999px;
                border: 2px solid #c1121f;
                background: #ffffff;
                margin-top: 0.35rem;
            }}
            .action-plan-copy {{
                color: #1f1f1f;
                line-height: 1.42;
                font-size: 1rem;
                font-weight: 600;
            }}
            .action-plan-target {{
                margin-top: 1rem;
                border-radius: 22px;
                padding: 1.15rem 1.2rem;
                background: linear-gradient(135deg, #111111 0%, #271014 100%);
                color: #ffffff;
                box-shadow: 0 18px 32px rgba(17, 17, 17, 0.12);
            }}
            .action-plan-target-kicker {{
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 0.74rem;
                font-weight: 800;
                color: #f5bcc0;
                margin-bottom: 0.5rem;
            }}
            .action-plan-target-copy {{
                font-size: 1.02rem;
                line-height: 1.4;
                font-weight: 700;
            }}
        </style>
        <div class="action-plan-stack">
            {action_items_html}
        </div>
        <div class="action-plan-target">
            <div class="action-plan-target-kicker">Key Target</div>
            <div class="action-plan-target-copy">{html.escape(ENGAGEMENT_KEY_TARGET)}</div>
        </div>
        """
    )


def render_engagement_infographic(section: dict) -> None:
    render_html(
        """
        <style>
            div[data-testid="stButton"] > button[kind="secondary"] {
                text-align: left;
            }
            div[data-testid="stButton"] > button {
                min-height: 132px;
                border-radius: 999px;
            }
        </style>
        """
    )
    center_col, steps_col = st.columns([1.05, 1.65], gap="large")
    with center_col:
        render_html(
            """
            <div class="infographic-core">
                <div class="ring ring-one"></div>
                <div class="ring ring-two"></div>
                <div class="ring ring-three"></div>
                <div class="ring ring-four"></div>
                <div class="core-card">
                    <h3>Client Engagement:<br>Greet &amp; Meet<br>Sessions</h3>
                </div>
            </div>
            """
        )
    with steps_col:
        for idx, ((heading, bullets), color) in enumerate(zip(section["content"], ENGAGEMENT_COLORS), start=1):
            left, right = st.columns([0.14, 0.86], gap="small")
            with left:
                render_html(
                    f"""
                    <div class="info-step-row">
                        <div class="step-number">{idx:02d}</div>
                    </div>
                    """
                )
            with right:
                label = heading
                if st.button(label, key=f"engagement-{idx}", use_container_width=True):
                    if heading == "Strategic Objectives":
                        show_strategic_objectives_dialog()
                    elif heading == "Current Engagement Status":
                        show_status_dialog()
                    elif heading == "Client Service Plan":
                        show_approach_dialog()
                    elif heading == "Action Plan":
                        show_action_plan_dialog()


def render_section_detail(section: dict) -> None:
    for heading, bullets in section["content"]:
        st.markdown(f"### {heading}")
        for bullet in bullets:
            st.markdown(f"- {bullet}")


def render_training_roadmap(section: dict) -> None:
    card_classes = ["roadmap", "objective", "audience", "delivery"]
    arrow_classes = ["orange", "green", "blue"]
    card_markup = []

    for idx, (heading, bullets) in enumerate(section["content"]):
        title_html = ""
        if idx > 0:
            title_html = f'<div class="training-card-title">{html.escape(heading)}:</div>'

        if heading in {"Target Audience", "Delivery Formats"}:
            copy_html = "<br>".join(html.escape(bullet) for bullet in bullets)
        else:
            copy_html = "<br><br>".join(html.escape(bullet) for bullet in bullets)

        card_markup.append(
            f'<div class="training-card training-card-{card_classes[idx]}">'
            f"{title_html}"
            f'<div class="training-card-copy">{copy_html}</div>'
            f"</div>"
        )

        if idx < len(section["content"]) - 1:
            card_markup.append(
                f'<div class="training-arrow training-arrow-{arrow_classes[idx]}" aria-hidden="true">'
                f"<span></span>"
                f"</div>"
            )

    cards_html = "".join(card_markup)
    continuation_markup = []

    for idx, item in enumerate(TRAINING_CONTINUATION_STEPS, start=1):
        tone_class = "dark" if idx % 2 == 0 else "light"
        continuation_markup.append(
            f'<div class="training-stage training-stage-{tone_class}">'
            f'<div class="training-stage-index">{idx:02d}</div>'
            f'<div class="training-stage-body">'
            f'<div class="training-stage-step">{html.escape(item["step"])}</div>'
            f'<div class="training-stage-action">{html.escape(item["action"])}</div>'
            f"</div>"
            f"</div>"
        )

    continuation_html = "".join(continuation_markup)

    render_html(
        f"""
        <style>
            .training-roadmap {{
                background: #ffffff;
                border: 1px solid rgba(17, 17, 17, 0.12);
                border-radius: 28px;
                padding: 2rem 1.6rem 2.2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 20px 40px rgba(17, 17, 17, 0.08);
            }}
            .training-roadmap-section-title {{
                margin: 0 0 0.9rem;
                font-size: 1.45rem;
                line-height: 1.08;
                color: #111111;
            }}
            .training-flow {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.65rem;
                flex-wrap: nowrap;
            }}
            .training-card {{
                box-sizing: border-box;
                flex: 1 1 0;
                max-width: 205px;
                min-width: 0;
                min-height: 360px;
                border-radius: 22px;
                border: 2px solid #111111;
                padding: 1.35rem 1.15rem;
                color: #ffffff;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0 20px 34px rgba(17, 17, 17, 0.14);
            }}
            .training-card-roadmap {{
                background: linear-gradient(180deg, #c1121f 0%, #e5383b 100%);
            }}
            .training-card-objective {{
                background: linear-gradient(180deg, #111111 0%, #2b2b2b 100%);
            }}
            .training-card-audience {{
                background: #ffffff;
                border-color: #c1121f;
                color: #111111;
            }}
            .training-card-delivery {{
                background: linear-gradient(180deg, #c1121f 0%, #9f0f18 100%);
            }}
            .training-card-title {{
                margin-bottom: 0.75rem;
                font-size: 1.05rem;
                font-style: italic;
                font-weight: 800;
                line-height: 1.2;
            }}
            .training-card-audience .training-card-title {{
                color: #c1121f;
            }}
            .training-card-copy {{
                font-size: 0.98rem;
                line-height: 1.34;
                font-weight: 600;
            }}
            .training-arrow {{
                width: 32px;
                flex: 0 0 32px;
                color: #c1121f;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .training-arrow span {{
                position: relative;
                display: block;
                width: 20px;
                height: 20px;
            }}
            .training-arrow span::before {{
                content: "";
                position: absolute;
                left: 0;
                top: 6px;
                width: 16px;
                height: 8px;
                border-radius: 2px;
                background: currentColor;
            }}
            .training-arrow span::after {{
                content: "";
                position: absolute;
                right: -2px;
                top: 0;
                border-left: 16px solid currentColor;
                border-top: 10px solid transparent;
                border-bottom: 10px solid transparent;
            }}
            .training-arrow-orange {{
                color: #c1121f;
            }}
            .training-arrow-green {{
                color: #111111;
            }}
            .training-arrow-blue {{
                color: #c1121f;
            }}
            details[data-testid="stExpander"] {{
                margin-top: 1.8rem;
                border: 1px solid rgba(17, 17, 17, 0.12);
                border-radius: 24px;
                background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
                box-shadow: 0 18px 35px rgba(17, 17, 17, 0.08);
                overflow: hidden;
            }}
            details[data-testid="stExpander"] summary {{
                background: linear-gradient(135deg, #111111 0%, #242424 100%);
                border-radius: 24px;
                padding: 0.3rem 0.8rem;
            }}
            details[data-testid="stExpander"][open] summary {{
                border-radius: 24px 24px 0 0;
            }}
            details[data-testid="stExpander"] summary:hover {{
                color: inherit;
            }}
            details[data-testid="stExpander"] summary p {{
                color: #ffffff;
                font-size: 1.18rem;
                font-weight: 800;
                letter-spacing: 0.03em;
            }}
            .training-expander-layout {{
                display: grid;
                grid-template-columns: minmax(240px, 300px) 1fr;
                gap: 1.25rem;
                align-items: start;
                padding-top: 0.35rem;
            }}
            .training-expander-intro {{
                position: relative;
                overflow: hidden;
                background: linear-gradient(180deg, #111111 0%, #242424 100%);
                color: #ffffff;
                border-radius: 22px;
                padding: 1.3rem 1.25rem 1.4rem;
                min-height: 100%;
            }}
            .training-expander-intro::after {{
                content: "";
                position: absolute;
                right: -22px;
                bottom: -38px;
                width: 150px;
                height: 150px;
                border-radius: 999px;
                background: radial-gradient(circle, rgba(229, 56, 59, 0.26) 0%, rgba(229, 56, 59, 0) 72%);
            }}
            .training-expander-kicker {{
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 0.72rem;
                font-weight: 800;
                color: #f4b6bb;
            }}
            .training-expander-intro h4 {{
                margin: 0.45rem 0 0.75rem;
                font-size: 1.45rem;
                line-height: 1.05;
            }}
            .training-expander-intro p {{
                margin: 0;
                max-width: 25ch;
                color: rgba(255, 255, 255, 0.86);
                line-height: 1.45;
                font-size: 0.96rem;
            }}
            .training-stages {{
                display: grid;
                gap: 0.9rem;
            }}
            .training-stage {{
                display: grid;
                grid-template-columns: 68px 1fr;
                gap: 1rem;
                align-items: center;
                border-radius: 22px;
                padding: 1rem 1.1rem;
                border: 1px solid rgba(17, 17, 17, 0.12);
                box-shadow: 0 16px 30px rgba(17, 17, 17, 0.08);
            }}
            .training-stage-light {{
                background: linear-gradient(180deg, #ffffff 0%, #f8f8f8 100%);
                color: #111111;
            }}
            .training-stage-dark {{
                background: linear-gradient(180deg, #151515 0%, #242424 100%);
                color: #ffffff;
            }}
            .training-stage-index {{
                width: 68px;
                height: 68px;
                border-radius: 20px;
                background: linear-gradient(180deg, #c1121f 0%, #e5383b 100%);
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                font-weight: 900;
                box-shadow: 0 14px 26px rgba(193, 18, 31, 0.24);
            }}
            .training-stage-body {{
                display: grid;
                gap: 0.3rem;
            }}
            .training-stage-step {{
                font-size: 1.02rem;
                font-weight: 900;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }}
            .training-stage-light .training-stage-step {{
                color: #c1121f;
            }}
            .training-stage-action {{
                font-size: 0.98rem;
                line-height: 1.35;
            }}
            @media (max-width: 1100px) {{
                .training-flow {{
                    gap: 1.15rem;
                }}
                .training-arrow {{
                    display: none;
                }}
                .training-card {{
                    width: min(100%, 280px);
                    min-height: 280px;
                }}
                .training-expander-layout {{
                    grid-template-columns: 1fr;
                }}
                .training-expander-intro p {{
                    max-width: none;
                }}
            }}
        </style>
        <div class="training-roadmap">
            <h3 class="training-roadmap-section-title">Training Vision</h3>
            <div class="training-flow">
                {cards_html}
            </div>
        </div>
        """
    )

    with st.expander("Training Roadmap In Motion", expanded=False):
        render_html(
            f"""
            <div class="training-expander-layout">
                <div class="training-expander-intro">
                    <div class="training-expander-kicker">Continuation</div>
                    <h4>From Discovery To Delivery</h4>
                    <p>We carry the plan forward from discovery during Greet &amp; Meet sessions into delivery and measurable learning outcomes.</p>
                </div>
                <div class="training-stages">
                    {continuation_html}
                </div>
            </div>
            """
        )


def _legacy_render_pipeline_landscape(section: dict) -> None:
    for heading, bullets in section["content"]:
        with st.expander(heading, expanded=False):
            for bullet in bullets:
                st.markdown(f"- {bullet}")

    return

    render_component_html(
        """
        <style>
            body {
                margin: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }
            .pipeline-hero {
                position: relative;
                min-height: 360px;
                overflow: hidden;
                border-radius: 28px;
                background:
                    radial-gradient(circle at 26% 62%, rgba(229, 56, 59, 0.14), transparent 14%),
                    radial-gradient(circle at 47% 48%, rgba(229, 56, 59, 0.1), transparent 10%),
                    radial-gradient(circle at 77% 28%, rgba(229, 56, 59, 0.12), transparent 14%),
                    linear-gradient(180deg, #111111 0%, #1a1a1a 52%, #252525 100%);
                border: 1px solid rgba(255,255,255,0.08);
            }
            .pipeline-hero::before {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(90deg, rgba(6, 12, 10, 0.42), rgba(6, 12, 10, 0.15)),
                    radial-gradient(circle at 18% 16%, rgba(255,255,255,0.07), transparent 18%);
            }
            .pipeline-glow {
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 32% 74%, rgba(255,255,255,0.08), transparent 18%),
                    radial-gradient(circle at 55% 74%, rgba(255,255,255,0.05), transparent 16%);
                filter: blur(10px);
            }
            .pipeline-link {
                position: absolute;
                border-top: 4px dashed rgba(255,255,255,0.88);
                z-index: 1;
            }
            .link-a {
                left: 16%;
                top: 56%;
                width: 18%;
                transform: rotate(-24deg);
            }
            .link-b {
                left: 39%;
                top: 36%;
                width: 15%;
                transform: rotate(21deg);
            }
            .link-c {
                left: 60%;
                top: 39%;
                width: 17%;
                transform: rotate(-22deg);
            }
            .pipeline-node {
                position: absolute;
                width: 154px;
                height: 154px;
                border-radius: 999px;
                border: 4px solid rgba(255,255,255,0.92);
                background: rgba(17, 17, 17, 0.42);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-shadow: 0 18px 40px rgba(0,0,0,0.2);
                z-index: 2;
            }
            .node-opportunity { left: 5%; top: 44%; }
            .node-market { left: 29%; top: 18%; }
            .node-solution { left: 51%; top: 40%; }
            .node-model {
                right: 5%;
                top: 10%;
                width: 180px;
                height: 180px;
            }
            .node-symbol {
                font-size: 2rem;
                line-height: 1;
                margin-bottom: 0.55rem;
                filter: grayscale(1) brightness(2.2);
            }
            .node-name {
                font-size: 1.22rem;
                line-height: 1.02;
                font-weight: 800;
                text-transform: uppercase;
            }
        </style>
        <div class="pipeline-hero">
            <div class="pipeline-glow"></div>
            <div class="pipeline-link link-a"></div>
            <div class="pipeline-link link-b"></div>
            <div class="pipeline-link link-c"></div>

            <div class="pipeline-node node-opportunity">
                <div class="node-symbol">◉</div>
                <div class="node-name">Opportunity</div>
            </div>

            <div class="pipeline-node node-market">
                <div class="node-symbol">▥</div>
                <div class="node-name">Market</div>
            </div>

            <div class="pipeline-node node-solution">
                <div class="node-symbol">⬢</div>
                <div class="node-name">Solution</div>
            </div>

            <div class="pipeline-node node-model">
                <div class="node-symbol">⚙</div>
                <div class="node-name">Business<br>Model</div>
            </div>
        </div>
        """,
        height=380,
    )

    render_html(
        """
        <div class="detail-card">
            <div class="detail-eyebrow">Selected Section</div>
            <h2>Active Leads<br>&amp; Pipelines</h2>
            <p>Current live opportunities, owners, and pipeline movement.</p>
        </div>
        """
    )

    for heading, bullets in section["content"]:
        with st.expander(heading, expanded=False):
            for bullet in bullets:
                st.markdown(f"- {bullet}")


def render_pipeline_landscape(section: dict) -> None:
    priority_html = "".join(
        f'<div class="pipeline-priority-card">{html.escape(item)}</div>'
        for item in section["content"][-1][1]
    )

    render_html(
        f"""
        <style>
            .pipeline-side {{
                position: relative;
                overflow: hidden;
                background: linear-gradient(165deg, #111111 0%, #161616 58%, #3a0e14 100%);
                color: #ffffff;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 1.5rem 1.35rem;
                min-height: 100%;
            }}
            .pipeline-side::after {{
                content: "";
                position: absolute;
                right: -36px;
                bottom: -36px;
                width: 170px;
                height: 170px;
                border-radius: 999px;
                background: radial-gradient(circle, rgba(229, 56, 59, 0.28) 0%, rgba(229, 56, 59, 0) 72%);
            }}
            .pipeline-side-kicker {{
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 0.72rem;
                font-weight: 800;
                color: #f5bcc0;
            }}
            .pipeline-side h3 {{
                margin: 0.75rem 0 0.85rem;
                font-size: clamp(2rem, 2.8vw, 3rem);
                line-height: 0.94;
            }}
            .pipeline-main {{
                padding: 0.8rem;
                background: linear-gradient(180deg, #ffffff 0%, #fcfcfc 100%);
            }}
            .pipeline-main-head {{
                padding: 0.2rem 0.2rem 0.9rem;
            }}
            .pipeline-main-head h4 {{
                margin: 0;
                font-size: 1.2rem;
                color: #111111;
            }}
            .pipeline-stage {{
                position: relative;
                border-radius: 28px;
                padding: 1.1rem 1.2rem 1.4rem;
                background:
                    radial-gradient(circle at 12% 10%, rgba(193, 18, 31, 0.12), transparent 42%),
                    radial-gradient(circle at 88% 6%, rgba(17, 17, 17, 0.08), transparent 40%),
                    #ffffff;
                border: 1px solid rgba(17, 17, 17, 0.16);
                box-shadow: 0 20px 34px rgba(17, 17, 17, 0.08);
            }}
            .pipeline-table-edit .stButton > button {{
                background: #111111;
                color: #ffffff;
                border-radius: 999px;
                padding: 0.65rem 1.4rem;
                border: 2px solid #111111;
                font-weight: 800;
            }}
            .pipeline-table-edit .stButton > button:hover {{
                background: #c1121f;
                border-color: #c1121f;
                color: #ffffff;
            }}
            .pipeline-priority {{
                margin-top: 1rem;
                padding: 0 0.2rem;
            }}
            .pipeline-priority h5 {{
                margin: 0 0 0.75rem;
                font-size: 1rem;
                color: #111111;
            }}
            .pipeline-priority-grid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.85rem;
            }}
            .pipeline-priority-card {{
                border-radius: 18px;
                padding: 0.95rem 1rem;
                background: linear-gradient(180deg, #ffffff 0%, #f7f7f7 100%);
                border: 1px solid rgba(17, 17, 17, 0.08);
                box-shadow: 0 14px 24px rgba(17, 17, 17, 0.05);
                line-height: 1.4;
                color: #222222;
            }}
            div[data-testid="stDataEditor"],
            div[data-testid="stDataFrame"],
            .stDataEditor,
            .stDataFrame {{
                border: 2px solid #c1121f !important;
                border-radius: 20px !important;
                overflow: hidden !important;
                background: #ffffff !important;
                box-shadow: 0 18px 30px rgba(17, 17, 17, 0.1) !important;
                max-width: 980px;
                margin: 0 auto;
                --dataframe-header-background-color: #111111;
                --dataframe-header-text-color: #ffffff;
                --dataframe-row-border-color: rgba(193, 18, 31, 0.35);
                --dataframe-row-hover-background-color: rgba(193, 18, 31, 0.16);
                --dataframe-row-background-color: #ffffff;
                --dataframe-row-alt-background-color: rgba(193, 18, 31, 0.08);
                --dataframe-text-color: #111111;
                --dataframe-border-color: rgba(193, 18, 31, 0.35);
            }}
            div[data-testid="stDataEditor"] [role="grid"],
            div[data-testid="stDataFrame"] [role="grid"],
            .stDataEditor [role="grid"],
            .stDataFrame [role="grid"] {{
                width: 100% !important;
            }}
            div[data-testid="stDataEditor"] [role="columnheader"],
            div[data-testid="stDataFrame"] [role="columnheader"],
            .stDataEditor [role="columnheader"],
            .stDataFrame [role="columnheader"] {{
                min-width: 0 !important;
                max-width: 1px !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"],
            div[data-testid="stDataFrame"] [role="gridcell"],
            .stDataEditor [role="gridcell"],
            .stDataFrame [role="gridcell"] {{
                min-width: 0 !important;
                max-width: 1px !important;
            }}
            div[data-testid="stDataEditor"] [role="grid"] div,
            div[data-testid="stDataFrame"] [role="grid"] div,
            .stDataEditor [role="grid"] div,
            .stDataFrame [role="grid"] div {{
                min-width: 0 !important;
            }}
            div[data-testid="stDataEditor"] [role="grid"],
            div[data-testid="stDataFrame"] [role="grid"],
            .stDataEditor [role="grid"],
            .stDataFrame [role="grid"] {{
                overflow-x: hidden !important;
            }}
            div[data-testid="stDataEditor"] [role="columnheader"],
            div[data-testid="stDataFrame"] [role="columnheader"],
            div[data-testid="stDataEditor"] [role="gridcell"],
            div[data-testid="stDataFrame"] [role="gridcell"],
            .stDataEditor [role="columnheader"],
            .stDataFrame [role="columnheader"],
            .stDataEditor [role="gridcell"],
            .stDataFrame [role="gridcell"] {{
                white-space: normal !important;
                word-break: break-word !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"] > div,
            div[data-testid="stDataFrame"] [role="gridcell"] > div,
            .stDataEditor [role="gridcell"] > div,
            .stDataFrame [role="gridcell"] > div {{
                white-space: normal !important;
                word-break: break-word !important;
            }}
            div[data-testid="stDataEditor"] [role="grid"],
            div[data-testid="stDataFrame"] [role="grid"],
            .stDataEditor [role="grid"],
            .stDataFrame [role="grid"] {{
                border: 0 !important;
            }}
            div[data-testid="stDataEditor"] [role="columnheader"],
            div[data-testid="stDataFrame"] [role="columnheader"],
            .stDataEditor [role="columnheader"],
            .stDataFrame [role="columnheader"] {{
                background: linear-gradient(180deg, #111111 0%, #1f1f1f 100%) !important;
                color: #ffffff !important;
                border-color: rgba(193, 18, 31, 0.6) !important;
                font-weight: 800 !important;
                letter-spacing: 0.01em !important;
                box-shadow: inset 0 -2px 0 rgba(193, 18, 31, 0.85);
            }}
            div[data-testid="stDataEditor"] [role="columnheader"] *,
            div[data-testid="stDataFrame"] [role="columnheader"] *,
            .stDataEditor [role="columnheader"] *,
            .stDataFrame [role="columnheader"] * {{
                color: #ffffff !important;
            }}
            div[data-testid="stDataEditor"] [role="columnheader"] svg,
            div[data-testid="stDataFrame"] [role="columnheader"] svg,
            .stDataEditor [role="columnheader"] svg,
            .stDataFrame [role="columnheader"] svg {{
                fill: #ffffff !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"],
            div[data-testid="stDataFrame"] [role="gridcell"],
            .stDataEditor [role="gridcell"],
            .stDataFrame [role="gridcell"] {{
                background: #ffffff !important;
                color: #111111 !important;
                border-color: rgba(193, 18, 31, 0.35) !important;
            }}
            div[data-testid="stDataEditor"] [role="row"]:nth-child(even) [role="gridcell"],
            div[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"],
            .stDataEditor [role="row"]:nth-child(even) [role="gridcell"],
            .stDataFrame [role="row"]:nth-child(even) [role="gridcell"] {{
                background: rgba(193, 18, 31, 0.18) !important;
            }}
            div[data-testid="stDataEditor"] [role="row"]:hover [role="gridcell"],
            div[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"],
            .stDataEditor [role="row"]:hover [role="gridcell"],
            .stDataFrame [role="row"]:hover [role="gridcell"] {{
                background: rgba(193, 18, 31, 0.28) !important;
            }}
            div[data-testid="stDataEditor"] [role="row"]:nth-child(even),
            div[data-testid="stDataFrame"] [role="row"]:nth-child(even),
            .stDataEditor [role="row"]:nth-child(even),
            .stDataFrame [role="row"]:nth-child(even) {{
                background: rgba(193, 18, 31, 0.18) !important;
            }}
            div[data-testid="stDataEditor"] [role="row"]:hover,
            div[data-testid="stDataFrame"] [role="row"]:hover,
            .stDataEditor [role="row"]:hover,
            .stDataFrame [role="row"]:hover {{
                background: rgba(193, 18, 31, 0.28) !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"][aria-selected="true"],
            div[data-testid="stDataFrame"] [role="gridcell"][aria-selected="true"],
            .stDataEditor [role="gridcell"][aria-selected="true"],
            .stDataFrame [role="gridcell"][aria-selected="true"] {{
                outline: 2px solid #c1121f !important;
                box-shadow: inset 0 0 0 2px rgba(193, 18, 31, 0.25) !important;
                background: #ffffff !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"]:focus,
            div[data-testid="stDataFrame"] [role="gridcell"]:focus,
            .stDataEditor [role="gridcell"]:focus,
            .stDataFrame [role="gridcell"]:focus {{
                outline: 2px solid #c1121f !important;
                outline-offset: -2px !important;
            }}
            div[data-testid="stDataEditor"] [role="gridcell"] a,
            div[data-testid="stDataFrame"] [role="gridcell"] a,
            .stDataEditor [role="gridcell"] a,
            .stDataFrame [role="gridcell"] a {{
                color: #c1121f !important;
                font-weight: 700 !important;
            }}
            div[data-testid="stDataEditor"] table,
            div[data-testid="stDataFrame"] table {{
                border-collapse: collapse !important;
            }}
            div[data-testid="stDataEditor"] thead tr th,
            div[data-testid="stDataFrame"] thead tr th {{
                background: #111111 !important;
                color: #ffffff !important;
                border-bottom: 2px solid #c1121f !important;
            }}
            div[data-testid="stDataEditor"] tbody tr td,
            div[data-testid="stDataFrame"] tbody tr td {{
                background: #ffffff !important;
                color: #111111 !important;
                border-bottom: 1px solid rgba(193, 18, 31, 0.3) !important;
            }}
            div[data-testid="stDataEditor"] tbody tr:nth-child(even) td,
            div[data-testid="stDataFrame"] tbody tr:nth-child(even) td {{
                background: rgba(193, 18, 31, 0.08) !important;
            }}
            div[data-testid="stDataEditor"] tbody tr:hover td,
            div[data-testid="stDataFrame"] tbody tr:hover td {{
                background: rgba(193, 18, 31, 0.16) !important;
            }}
            @media (max-width: 1080px) {{
                .pipeline-priority-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """
    )

    _, main_col, _ = st.columns([1, 3, 1], gap="large")
    with main_col:
        render_html('<div class="pipeline-stage">')
        render_html(
            """
            <div class="pipeline-main-head">
                <h4>Opportunity Tracker</h4>
            </div>
            """
        )

        if "pipeline_saved" not in st.session_state:
            st.session_state.pipeline_saved = False

        if st.session_state.pipeline_saved:
            st.success("Changes saved.")
            st.session_state.pipeline_saved = False

        table_rows = get_pipeline_table()
        columns = [
            ("client", "Client"),
            ("income", "Income"),
            ("progress", "Progress"),
            ("estimated_placement", "Estimated Placement Dates"),
            ("comments", "Comments"),
            ("responsible_person", "Responsible Person"),
        ]

        with st.form("pipeline_editor_form", clear_on_submit=False):
            table_df = pd.DataFrame(table_rows)
            edited_df = st.data_editor(
                table_df,
                hide_index=True,
                use_container_width=True,
                num_rows="fixed",
                column_order=[col for col, _ in columns],
                column_config={
                    "client": st.column_config.TextColumn("Client"),
                    "income": st.column_config.TextColumn(
                        "Income",
                        help="Enter premium/fee or keep TBD.",
                    ),
                    "progress": st.column_config.TextColumn("Progress"),
                    "estimated_placement": st.column_config.TextColumn(
                        "Estimated Placement Dates",
                        help="Enter date/time when available (e.g., 2026-03-21 14:00).",
                    ),
                    "comments": st.column_config.TextColumn("Comments"),
                    "responsible_person": st.column_config.TextColumn("Responsible Person"),
                },
                disabled=["client", "progress", "comments", "responsible_person"],
                height=420,
                key="pipeline_editor",
            )
            save_changes = st.form_submit_button("Save changes")
        if save_changes:
            st.session_state.pipeline_table = edited_df.to_dict(orient="records")
            st.session_state.pipeline_saved = True
            st.rerun()

        render_html(
            f"""
            <div class="pipeline-priority">
                <h5>{html.escape(section["content"][-1][0])}</h5>
                <div class="pipeline-priority-grid">
                    {priority_html}
                </div>
            </div>
            """
        )
        render_html("</div>")


render_html(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #fafafa 0%, #f1f1f1 100%);
            color: #111111;
        }
        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .intro-card {
            position: relative;
            overflow: hidden;
            display: grid;
            grid-template-columns: minmax(180px, 220px) minmax(0, 1fr);
            align-items: center;
            gap: 1.35rem;
            background:
                radial-gradient(circle at 12% 18%, rgba(255, 255, 255, 0.08), transparent 14%),
                radial-gradient(circle at 86% 18%, rgba(229, 56, 59, 0.2), transparent 16%),
                linear-gradient(135deg, #0e0e0f 0%, #171717 48%, #241013 100%);
            color: #ffffff;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1rem 1.2rem;
            margin-bottom: 2rem;
            box-shadow: 0 24px 48px rgba(17, 17, 17, 0.2);
        }
        .intro-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(120deg, rgba(255, 255, 255, 0.04), transparent 24%),
                repeating-linear-gradient(
                    -36deg,
                    rgba(255, 255, 255, 0.02) 0,
                    rgba(255, 255, 255, 0.02) 2px,
                    transparent 2px,
                    transparent 16px
                );
            pointer-events: none;
        }
        .intro-card::after {
            content: "";
            position: absolute;
            right: -52px;
            top: -56px;
            width: 180px;
            height: 180px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(229, 56, 59, 0.22) 0%, rgba(229, 56, 59, 0) 72%);
        }
        .intro-card-no-logo {
            grid-template-columns: minmax(0, 1fr);
        }
        .intro-logo {
            position: relative;
            z-index: 1;
            flex: 0 0 auto;
            width: 200px;
            height: 104px;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(244, 244, 244, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.8rem;
            box-shadow: 0 16px 28px rgba(0, 0, 0, 0.18);
        }
        .intro-logo img {
            width: 100%;
            height: auto;
            object-fit: contain;
        }
        .intro-copy {
            position: relative;
            z-index: 1;
            min-width: 0;
            display: grid;
            gap: 0.65rem;
            align-content: center;
        }
        .intro-card h1 {
            margin: 0;
            font-size: clamp(1.9rem, 3.8vw, 3.1rem);
            line-height: 0.94;
            letter-spacing: -0.04em;
            max-width: none;
            text-wrap: balance;
        }
        .intro-divider {
            width: min(170px, 32vw);
            height: 3px;
            border-radius: 999px;
            background: linear-gradient(90deg, #e5383b 0%, rgba(229, 56, 59, 0.18) 100%);
        }
        .intro-pill-row {
            display: flex;
            gap: 0.65rem;
            flex-wrap: wrap;
        }
        .intro-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 0.38rem 0.72rem;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f4f4f4;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }
        .intro-pill-accent {
            background: rgba(229, 56, 59, 0.18);
            border-color: rgba(229, 56, 59, 0.3);
        }
        .detail-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(17, 17, 17, 0.12);
            border-radius: 24px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.5rem;
        }
        .detail-card h2 {
            margin: 0.2rem 0 0.5rem;
            line-height: 1.05;
        }
        .detail-card p {
            margin: 0;
            color: #333333;
        }
        .detail-eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-size: 0.74rem;
            color: #c1121f;
            font-weight: 800;
        }
        .infographic-core {
            position: relative;
            min-height: 420px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .core-card {
            width: 250px;
            height: 250px;
            border-radius: 999px;
            background: rgba(255,255,255,0.98);
            border: 6px solid #e5e5e5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 1.5rem;
            position: relative;
            z-index: 2;
            box-shadow: 0 18px 35px rgba(17, 17, 17, 0.08);
        }
        .core-card h3 {
            margin: 0;
            color: #111111;
            font-size: 1.25rem;
            line-height: 1.12;
        }
        .ring {
            position: absolute;
            inset: 50%;
            translate: -50% -50%;
            border-radius: 999px;
            border: 4px solid transparent;
        }
        .ring-one {
            width: 290px;
            height: 290px;
            border-top-color: #111111;
            border-right-color: #111111;
        }
        .ring-two {
            width: 330px;
            height: 330px;
            border-right-color: #c1121f;
            border-bottom-color: #c1121f;
        }
        .ring-three {
            width: 370px;
            height: 370px;
            border-bottom-color: #2b2b2b;
            border-left-color: #2b2b2b;
        }
        .ring-four {
            width: 410px;
            height: 410px;
            border-left-color: #e5383b;
            border-top-color: #e5383b;
        }
        .info-step-row {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            margin-bottom: 1rem;
        }
        .step-number {
            width: 58px;
            height: 58px;
            border-radius: 999px;
            background: #ffffff;
            border: 2px solid rgba(17, 17, 17, 0.14);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: #111111;
            box-shadow: 0 10px 20px rgba(17, 17, 17, 0.08);
            flex: 0 0 auto;
        }
        .step-pill {
            border-radius: 999px;
            padding: 0.95rem 1.25rem;
            color: white;
            box-shadow: 0 14px 28px rgba(17, 17, 17, 0.12);
        }
        .step-title {
            font-weight: 800;
            margin-bottom: 0.25rem;
        }
        .step-copy {
            font-size: 0.92rem;
            line-height: 1.35;
            color: rgba(255,255,255,0.94);
        }
        .objective-row {
            display: flex;
            justify-content: center;
            gap: 1.25rem;
            align-items: flex-start;
            flex-wrap: wrap;
        }
        .top-row {
            margin-top: 0.75rem;
            margin-bottom: 1.1rem;
        }
        .bottom-row {
            gap: 1.6rem;
            justify-content: center;
        }
        .objective-box {
            position: relative;
            padding: 1.35rem 1.1rem 1rem;
            border: 2px solid #111111;
            border-radius: 28px;
            background: #ffffff;
            text-align: center;
            line-height: 1.25;
            box-shadow: 0 14px 28px rgba(17, 17, 17, 0.08);
        }
        .objective-box::before {
            content: "";
            position: absolute;
            left: 18px;
            right: 18px;
            top: 12px;
            height: 8px;
            border-radius: 999px;
            background: linear-gradient(90deg, #111111 0%, #c1121f 100%);
            opacity: 0.95;
        }
        .objective-box.narrow {
            width: 180px;
        }
        .objective-box.wide {
            width: 260px;
        }
        .objective-connector {
            margin: 0 auto;
            background: #c1121f;
        }
        .objective-connector-main {
            display: none;
        }
        .objective-connector-mid {
            display: none;
        }
        .status-table-wrap {
            padding: 1rem 0.25rem 0.5rem;
        }
        .status-overview {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }
        .status-chip {
            border-radius: 999px;
            padding: 0.5rem 0.8rem;
            font-size: 0.86rem;
            font-weight: 800;
            color: #111111;
        }
        .status-chip.complete {
            background: #f1d0d3;
        }
        .status-chip.waiting {
            background: #e7e7e7;
        }
        .status-chip.progress {
            background: #d9d9d9;
        }
        .status-bar {
            flex: 1 1 220px;
            height: 14px;
            border-radius: 999px;
            background: #e5e5e5;
            overflow: hidden;
        }
        .status-bar-fill {
            width: 62%;
            height: 100%;
            background: linear-gradient(90deg, #111111 0%, #c1121f 100%);
        }
        .status-table-pretty {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            overflow: hidden;
            border-radius: 20px;
        }
        .status-table-pretty th,
        .status-table-pretty td {
            border: 2px solid #d32f2f;
            padding: 1rem 1rem;
            text-align: left;
            vertical-align: middle;
        }
        .status-table-pretty th {
            background: #111111;
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 800;
        }
        .status-table-pretty td {
            background: #ffffff;
            color: #111111;
            font-size: 0.98rem;
            line-height: 1.35;
            transition: background 0.2s ease, transform 0.2s ease;
        }
        .status-table-pretty tbody tr:hover td {
            background: #f9e2e4;
        }
        .approach-flow {
            position: relative;
            padding: 0.75rem 0.25rem 0.25rem;
        }
        .approach-lane {
            position: absolute;
            left: 28px;
            top: 18px;
            bottom: 18px;
            width: 4px;
            border-radius: 999px;
            background: linear-gradient(180deg, #111111 0%, #c1121f 100%);
        }
        .approach-stage {
            position: relative;
            display: grid;
            grid-template-columns: 72px 1fr;
            gap: 0.9rem;
            align-items: start;
            margin-bottom: 1rem;
        }
        .approach-dot {
            width: 56px;
            height: 56px;
            border-radius: 999px;
            background: #111111;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            position: relative;
            z-index: 1;
            box-shadow: 0 10px 20px rgba(17, 17, 17, 0.12);
        }
        .approach-panel {
            border: 2px solid #111111;
            border-radius: 22px;
            background: linear-gradient(180deg, #ffffff 0%, #f6f6f6 100%);
            padding: 0.95rem 1rem;
            box-shadow: 0 12px 24px rgba(17, 17, 17, 0.08);
        }
        .approach-heading {
            font-size: 1rem;
            font-weight: 900;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
            color: #c1121f;
        }
        .approach-text {
            font-size: 0.95rem;
            line-height: 1.3;
            color: #222222;
        }
        .approach-text ul.approach-bullets {
            margin: 0.35rem 0 0;
            padding-left: 1.1rem;
            display: grid;
            gap: 0.35rem;
        }
        .approach-text ul.approach-bullets li {
            margin: 0;
        }
        .pipeline-hero {
            position: relative;
            min-height: 360px;
            margin-bottom: 1.5rem;
            overflow: hidden;
            border-radius: 28px;
            background:
                radial-gradient(circle at 26% 62%, rgba(196, 235, 147, 0.18), transparent 14%),
                radial-gradient(circle at 47% 48%, rgba(196, 235, 147, 0.12), transparent 10%),
                radial-gradient(circle at 77% 28%, rgba(196, 235, 147, 0.16), transparent 14%),
                linear-gradient(180deg, #1a211a 0%, #121713 52%, #162018 100%);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .pipeline-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(6, 12, 10, 0.42), rgba(6, 12, 10, 0.15)),
                radial-gradient(circle at 18% 16%, rgba(255,255,255,0.07), transparent 18%);
        }
        .pipeline-glow {
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 32% 74%, rgba(255,255,255,0.08), transparent 18%),
                radial-gradient(circle at 55% 74%, rgba(255,255,255,0.05), transparent 16%);
            filter: blur(10px);
        }
        .pipeline-link {
            position: absolute;
            border-top: 4px dashed rgba(255,255,255,0.88);
            z-index: 1;
        }
        .link-a {
            left: 16%;
            top: 56%;
            width: 18%;
            transform: rotate(-24deg);
        }
        .link-b {
            left: 39%;
            top: 36%;
            width: 15%;
            transform: rotate(21deg);
        }
        .link-c {
            left: 60%;
            top: 39%;
            width: 17%;
            transform: rotate(-22deg);
        }
        .pipeline-node {
            position: absolute;
            width: 154px;
            height: 154px;
            border-radius: 999px;
            border: 4px solid rgba(255,255,255,0.92);
            background: rgba(10, 17, 14, 0.22);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 18px 40px rgba(0,0,0,0.2);
            z-index: 2;
        }
        .node-opportunity { left: 5%; top: 44%; }
        .node-market { left: 29%; top: 18%; }
        .node-solution { left: 51%; top: 40%; }
        .node-model {
            right: 5%;
            top: 10%;
            width: 180px;
            height: 180px;
        }
        .node-symbol {
            font-size: 2rem;
            line-height: 1;
            margin-bottom: 0.55rem;
            filter: grayscale(1) brightness(2.2);
        }
        .node-name {
            font-size: 1.22rem;
            line-height: 1.02;
            font-weight: 800;
            text-transform: uppercase;
        }
        div[data-testid="stPopover"] > button {
            min-height: 46px;
            border-radius: 999px;
            border: 1.5px solid rgba(17, 17, 17, 0.18);
            background: #ffffff;
            color: #111111;
            font-weight: 800;
            font-size: 0.92rem;
            line-height: 1;
            padding: 0.65rem 1.1rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            white-space: nowrap;
            box-shadow: 0 10px 22px rgba(17, 17, 17, 0.08);
        }
        div[data-testid="stPopover"] > button:hover {
            border-color: #c1121f;
            background: #fff6f6;
            color: #c1121f;
        }
        div[data-testid="stPopover"] > button p {
            margin: 0;
        }
        div[data-testid="stButton"] > button {
            min-height: 150px;
            border-radius: 22px;
            border: 2px solid #111111;
            background: rgba(201, 206, 210, 0.9);
            color: #000000;
            font-weight: 800;
            font-size: 1.05rem;
            line-height: 1.2;
            white-space: pre-line;
            box-shadow: inset 0 0 0 9999px rgba(255,255,255,0.1);
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #c1121f;
            color: #c1121f;
        }
        div[data-testid="stButton"] > button[kind="tertiary"] {
            min-height: 46px;
            min-width: 118px;
            border-radius: 999px;
            border: 1px solid rgba(17, 17, 17, 0.14);
            background: #ffffff;
            color: #111111;
            font-size: 0.94rem;
            font-weight: 700;
            line-height: 1;
            padding: 0.7rem 1.05rem;
            box-shadow: 0 10px 22px rgba(17, 17, 17, 0.08);
        }
        div[data-testid="stButton"] > button[kind="tertiary"]:hover {
            border-color: #c1121f;
            background: #fff6f6;
            color: #c1121f;
        }
        div[data-testid="stButton"] > button[kind="tertiary"]:disabled {
            background: #f2f2f2;
            color: #9a9a9a;
            border-color: rgba(17, 17, 17, 0.08);
            box-shadow: none;
        }
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: rgba(201, 206, 210, 0.9);
        }
        div[data-testid="stButton"] button p {
            margin: 0;
        }
        @media (max-width: 720px) {
            .intro-card {
                grid-template-columns: 1fr;
                align-items: flex-start;
            }
            .intro-logo {
                width: 88px;
                height: 88px;
            }
        }
    </style>
    """
)

if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

logo_markup = ""
if LOGO_BASE64:
    logo_markup = (
        f'<div class="intro-logo">'
        f'<img src="data:image/png;base64,{LOGO_BASE64}" alt="Minet logo">'
        f"</div>"
    )

intro_card_class = "intro-card"
if not LOGO_BASE64:
    intro_card_class += " intro-card-no-logo"

render_html(
    f'<div class="{intro_card_class}">'
    f"{logo_markup}"
    f'<div class="intro-copy">'
    f"<h1>Mining War Room</h1>"
    f'<div class="intro-divider"></div>'
    f'<div class="intro-pill-row">'
    f'<span class="intro-pill">Client Engagement</span>'
    f'<span class="intro-pill intro-pill-accent">Training Roadmap</span>'
    f'<span class="intro-pill">Active Pipeline</span>'
    f"</div>"
    f"</div>"
    f"</div>"
)

if st.session_state.selected_section is None:
    cols = st.columns(3, gap="large")
    for col, section in zip(cols, SECTIONS):
        with col:
            if st.button(section["title"], key=section["id"], use_container_width=True):
                st.session_state.selected_section = section["id"]
                st.rerun()
else:
    selected = next(section for section in SECTIONS if section["id"] == st.session_state.selected_section)
    if selected["id"] == "engagement":
        render_engagement_infographic(selected)
    elif selected["id"] == "training":
        render_training_roadmap(selected)
    elif selected["id"] == "pipeline":
        render_pipeline_landscape(selected)
    else:
        render_section_detail(selected)

    current_index = SECTION_ORDER.index(selected["id"])
    nav_left, nav_mid, nav_right = st.columns([1, 3, 1])
    with nav_left:
        if st.button("Previous", type="tertiary", disabled=current_index == 0):
            st.session_state.selected_section = SECTION_ORDER[current_index - 1]
            st.rerun()
    with nav_mid:
        if st.button("Back to Start", type="tertiary", use_container_width=True):
            st.session_state.selected_section = None
            st.rerun()
    with nav_right:
        if st.button("Next", type="tertiary", disabled=current_index == len(SECTION_ORDER) - 1):
            st.session_state.selected_section = SECTION_ORDER[current_index + 1]
            st.rerun()
