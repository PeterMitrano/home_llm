# Design

After 1 hour (or some other time) of inactivity, we start a new chat.
We probably new two levels of LLM, because LLMs do not have infinite memory or context length,
and since the API documentation for a given home device can be long, we need to break things down.
One LLM can used to generate code queries for a given device/API (e.g. LIFX, or Meross, etc...).
That LLM will start a new chat every time, and receive the API docs for that device in its prompt.
That complicates allowing the system to learn though... if we want to teach the device-LLM, we need to change its prompt instead of relying on ICL.
So that means the user or maybe the main LLM will need to be able to adjust the prompt used by the device LLM.
Anyway, the main LLM will have a basic system prompt to start each new interaction.