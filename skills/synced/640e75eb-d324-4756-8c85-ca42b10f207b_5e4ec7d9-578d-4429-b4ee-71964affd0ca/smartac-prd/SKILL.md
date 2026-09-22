---
name: smartac-prd
description: "Write Product Requirements Documents (PRDs) using SmartAC's official template. Use this skill whenever Cloe asks to write, draft, start, or create a PRD, requirements doc, or product spec — even if she doesn't say 'PRD' explicitly. Also trigger when she says things like 'help me write up requirements for X', 'I need a spec for Y', or 'let's document the requirements for Z'. Always use this skill rather than free-forming a document structure."
---

# SmartAC PRD Skill

## Template

1. **Setting the Stage** *(context for Eng)*
   - Current State — short description of where things are today
   - Desired End State — short description of the goal
   - Out of Scope Items
   - Definitions (as needed)

2. **Current State**
   - How It Works Now
   - Pain Points

3. **Motivation** *(contextual)*
   - User Insights/Data (quotes, tickets, metrics) — as needed
   - Impact/Opportunity Size — optional
   - User Stories, Use Cases, and UX Improvements

4. **Requirements**
   - Functional Requirements (existing functionality to enable & new functionality; serves as Acceptance Criteria)
   - Success Metrics — omit in initial Project Alpha infra-focused stages

5. **Open Questions & Next Steps** *(Prod and Eng fill out together during PRD review)*

6. **Phases** *(if necessary; filled out collaboratively as scope evolves)*

7. **Appendices for Context**

## Step 1: Gather Context

Before writing, make sure you have:
- **Feature/goal**: What is this PRD for?
- **Key stakeholders**: Who are the affected user roles (contractor, tech, homeowner, Member Success, etc.)?
- **Known context**: Pull from Granola, Linear, Notion, or the current conversation as relevant.
- **Any open questions Cloe has flagged**: Include them in section 5.

If Cloe gives you a topic but minimal detail, write a solid draft using what you know about SmartAC's context, and clearly mark placeholder sections for her to fill in.

## Step 2: Write the PRD

Follow the template structure exactly — don't add or remove top-level sections without a reason. Within sections, apply SmartAC's patterns:

- **Be concrete**: Name specific user roles (contractor CSR, technician, homeowner, Member Success), systems (ServiceTitan, ProApp, NOC, HomeApp, Contractor Dashboard), and known data objects (sensor cohort, subscription, membership, etc.)
- **Functional requirements**: Use numbered subsections (1.1, 1.2...) for anything with multiple states, rules, or entities
- **Open Questions table**: Always include columns: #, Question, Owner, Priority, Notes
- **State tables**: If the feature involves stateful objects, include a state table with State and Definition columns

## Step 3: Output Format

Default output is a well-formatted markdown document, ready to paste into Notion. If Cloe asks to create it directly in Notion, use the `notion-create-pages` tool and place it under the appropriate parent page.

For Notion creation:
- Parent default: Product Team Home > Process, Roles, & Reference Docs (unless Cloe specifies otherwise)
- Title format: `[Emoji] [Feature Name] Requirements` or `[Emoji] Project Alpha [Feature Name] Requirements`
- Use a relevant emoji for the icon
