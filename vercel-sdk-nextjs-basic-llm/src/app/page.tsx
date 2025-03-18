'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({maxSteps: 6});

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto">
      <div className="flex flex-col space-y-4 px-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-lg text-white max-w-xs md:max-w-sm shadow-md ${
                message.role === "user"
                  ? "bg-blue-500 text-right" 
                  : "bg-gray-700 text-left"
              }`}
            >
              {message.parts.map((part, i) => {
                switch(part.type){
                  case 'text':
                    return <div key={`${message.id}-${i}`} className="whitespace-pre-wrap">
                        {part.text}
                      </div>
                  case 'tool-invocation':
                    return <pre key={`${message.id}-${i}`}>
                    {JSON.stringify(part.toolInvocation, null, 2)}
                  </pre>
                }
                })}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="fixed bottom-0 w-full max-w-md mx-auto p-4 bg-white dark:bg-zinc-900">
        <div className="flex items-center border border-zinc-300 dark:border-zinc-800 rounded-lg shadow-md">
          <input
            className="flex-1 p-3 rounded-l-lg bg-transparent focus:outline-none"
            value={input}
            placeholder="Say something..."
            onChange={handleInputChange}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
          >
            ➤
          </button>
        </div>
      </form>
    </div>
  );
}
