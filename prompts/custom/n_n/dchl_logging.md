# Deferred Call Hierarchy Logging (DCHL)

## How It Works
*   **CallLog Object:** Acts as a centralized collector that tracks method execution flow.
*   **Entry Points:** Each method adds its signature to the call hierarchy using `log.addEntry()`.
*   **Deferred Output:** Instead of logging immediately, the complete call flow is displayed at the end.
*   **Clean Separation:** Business logic remains uncluttered with logging statements.

## Pros
*   **Clean Code:** Business logic isn't polluted with logging statements.
*   **Complete Flow Visibility:** Shows the entire execution path in one place.
*   **Performance:** No I/O operations during execution, only at the end.
*   **Centralized Control:** Easy to enable/disable logging globally.
*   **Readable Output:** Clear hierarchical view of method calls.
*   **Debugging Friendly:** Easy to trace execution flow for complex algorithms.
*   **Non-Intrusive:** Minimal impact on existing code structure.

## Cons
*   **Memory Overhead:** Stores all call information in memory.
*   **Lost on Exceptions:** If application crashes, call history might be lost.
*   **Manual Maintenance:** Requires developers to remember adding entries.
*   **Limited Context:** Doesn't capture parameter values or execution time.
*   **Scalability Issues:** Memory consumption grows with call depth.

---

## Master Prompt for AI Conversion

**TASK:** Convert existing Java project to Deferred Call Hierarchy Logging (DCHL) pattern.

**OBJECTIVE:** Transform traditional logging approach to a clean, deferred call hierarchy logging system.

**REQUIREMENTS:**

1.  **Create CallLog Infrastructure:**
    *   Create a `CallLog.java` class.
    *   `List<String> callHierarchy` to store method calls.
    *   `addEntry(String className, String methodName)` method.
    *   `getCallHierarchy()` method returning formatted string with `->` separator.

2.  **Modify Main Entry Points:**
    *   Instantiate `CallLog log = new CallLog();` in main method.
    *   Add entry: `log.addEntry("Main", "main()");`
    *   Pass `log` object to all subsequent methods.
    *   Display final hierarchy: `System.out.println("API Flow: " + log.getCallHierarchy());`

3.  **Transform All Methods:**
    *   Add `CallLog log` parameter to all business methods.
    *   Add `log.addEntry(this.getClass().getSimpleName(), "methodName()");` as FIRST line.
    *   Keep only `logger.error` for exceptions.
    *   Pass `log` object to all downstream method calls.

4.  **Method Entry Pattern:**
    ```java
    public ReturnType methodName(params..., CallLog log) {
        log.addEntry(this.getClass().getSimpleName(), "methodName()");
        // existing business logic without logging
    }
    ```

5.  **Preserve:**
    *   All business logic unchanged.
    *   Exception handling and error logging.
    *   Final result logging (can be kept separate from flow tracing).

6.  **Guidelines:**
    *   Use `this.getClass().getSimpleName()` for class names.
    *   Use exact method names in quotes.
    *   Maintain consistent parameter ordering (business params first, log last).
    *   Remove intermediate debug/info logs that clutter business logic.
    *   Keep performance-critical sections clean.

**OUTPUT:** Provide the converted code maintaining the same business functionality but with clean, deferred call hierarchy logging pattern.

**NOTE:** This pattern is particularly effective for algorithmic trading systems, financial calculations, or any complex business logic where understanding the exact execution flow is crucial but you want to keep the core logic clean and readable.
