
---
description: Add Python class and function header comments in a specific visual style
argument-hint: Specify style (HashBlock, AsciiBox...) and target (active file, folder...)
agent: agent
tools: []
---
Make sure user provided style in ${input:style} and target in ${input:target}. If not, do not continue and ask for them again.

The `target` input specifies the scope of the operation. It can be:
- "active file" or "current file"
- A specific file path
- A directory path (to apply to all files in that directory)
- A glob pattern (e.g., "**/*.py")

Based on the style provided, add visual function header comments before each function definition or class in the Python files specified by `target`. 
If there are already header comments present, replace them with the new style.

Use the following definitions for the styles:

1. **HashBlock**:
   ```python
   ###############################################################################
   # FUNCTION NAME
   ###############################################################################
   ```

2. **AsciiBox**:
   ```python
   # +-----------------------------------------------------------------------------+
   # |                                FUNCTION NAME                                |
   # +-----------------------------------------------------------------------------+
   ```

3. **ArrowSeparator**:
   ```python
   # -----------------------------> FUNCTION NAME <-----------------------------
   ```

4. **DoubleDashBlock**:
   ```python
   # =============================================================================
   # FUNCTION NAME
   # =============================================================================
   ```

5. **StarBanner**:
   ```python
   # ****************************** FUNCTION NAME ******************************
   ```

6. **Minimal**:
   ```python
   # --- FUNCTION NAME ---
   ```

Apply the selected style to all Python functions and classes in the files matching the `target`.