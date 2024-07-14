# Design

After 1 hour (or some other time) of inactivity, we start a new chat.
We probably new two levels of LLM, because LLMs do not have infinite memory or context length,
and since the API documentation for a given home device can be long, we need to break things down.
One LLM can used to generate code queries for a given device/API (e.g. LIFX, or Meross, etc...).
That LLM will start a new chat every time, and receive the API docs for that device in its prompt.
That complicates allowing the system to learn though... if we want to teach the device-LLM, we need to change its prompt instead of relying on ICL.
So that means the user or maybe the main LLM will need to be able to adjust the prompt used by the device LLM.
Anyway, the main LLM will have a basic system prompt to start each new interaction.

Since the coding LLM will initially make mistakes on unfamiliar devices, we need a way to correct it.
I think we can consider two types of errors, one which is code that fails to run, and one that runs but does the wrong thing.
The user will need to help correct when it does the wrong thing, but code failures we can probably resolve autonomously.
To resolve cod errors, we could try to iteratively feed in the error the code produces, and get a new response.
Once it succeeds, we can treat this as a new training example and run fine-tuning.
GPT4All doesn't include finetuning as far as I can tell, so I'll have to figure out some way to do that later.