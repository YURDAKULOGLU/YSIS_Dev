# Summary: AI Theme Generation Architecture

This document outlines the architecture for enabling AI-generated, dynamic themes within the YBIS application.

## **Vision**
The goal is for the AI to dynamically generate and apply custom themes based on user prompts, seamlessly integrating with the application's existing navigation.

---

## **Current State (Static Theming)**
- The application currently uses static Light/Dark themes provided by Tamagui.
- Custom theme files (e.g., `ocean.theme.ts`) are prepared but not yet actively used due to Tamagui's specific token structure requirements.
- The theme store is ready for expansion, currently supporting Light/Dark selection.

---

## **AI-Ready System (Dynamic Theming Components)**

The proposed dynamic theming system comprises several key components:

1.  **Theme Schema (`ThemeSchema.ts`):** A JSON-serializable interface defining all properties of a theme, primarily focusing on a comprehensive color palette (background, foreground, text, grays, brand, status, UI, shadows). It also includes metadata like `id`, `name`, `author`, `createdAt`, and `description`.

2.  **Theme Store (`useThemeStore.ts`):** A runtime management store that holds both built-in (`systemThemes`) and dynamically created (`customThemes` by user/AI) themes. It provides actions to add, remove, update, and activate themes, as well as AI-specific actions for generation and saving.

3.  **AI Theme Generation Flow:** A sequence where a user's natural language prompt (e.g., "Create a cyberpunk neon theme") triggers an AI agent to call a theme generation function. The generated theme is then added to the `ThemeStore` and activated, instantly updating the UI.

4.  **AI Theme Generator Function (`generateTheme.ts`):** An asynchronous function (`generateThemeFromPrompt`) that takes a user prompt and an AI client. It uses a detailed system prompt (acting as a UI/UX color designer) to instruct the AI (e.g., Claude-3.5-Sonnet) to produce a `ThemeSchema` JSON. This function includes requirements for valid hex codes, WCAG AA accessibility contrast, harmonious gradients, and schema validation.

5.  **Persistence Layer:** Custom themes are saved to `AsyncStorage` to ensure they persist across app restarts, allowing users to retain their AI-generated themes.

6.  **UI: Theme Picker Screen (`ThemePickerScreen.tsx`):** A dedicated screen provides a user interface for generating themes via an input prompt and displaying available system and custom themes. It includes functionality for theme selection and deletion (for AI-generated themes).

---

## **Implementation Steps (Phased Approach)**
The implementation is planned in three phases:
1.  **Foundation:** Create `ThemeSchema`, migrate existing themes, update `ThemeStore`, and implement `AsyncStorage` persistence.
2.  **UI:** Develop `ThemePickerScreen`, theme preview cards, and theme deletion functionality.
3.  **AI Integration:** Implement the `generateTheme` function, focus on prompt engineering for color theory, add validation/contrast checking, and potentially theme refinement based on user feedback.

---

## **AI Agent Capabilities**
The system enables the AI agent to:
- Generate new themes from natural language descriptions.
- Modify existing themes (e.g., make a theme darker).
- Analyze the current theme's color palette.
- Recommend themes based on context (e.g., "theme for late night reading").

---

## **Benefits**
The AI theme generation system offers numerous benefits:
- **Dynamic & Unlimited Themes:** Themes can be generated on-the-fly without code changes.
- **Natural Language Interaction:** Users can describe themes intuitively.
- **Persistence & Shareability:** Themes are saved and can be exported/imported.
- **Real-time Preview:** Instant visual feedback.
- **Accessibility:** AI assists in ensuring WCAG contrast standards.

---

**Status:** Design phase. Next steps involve implementing `ThemeSchema` and migrating existing themes.
