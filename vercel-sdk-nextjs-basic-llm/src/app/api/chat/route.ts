import { openai } from '@ai-sdk/openai';
import { streamText, tool } from 'ai';
import { z } from 'zod';

export const maxDuration = 40;
const ETHERSCAN_KEY = process.env.ETHERSCAN_API_KEY ?? "";

export async function POST(req: Request) {
  if (!ETHERSCAN_KEY) {
      throw new Error("Missing ETHERSCAN_API_KEY in environment variables");
  }

  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
        weather: tool({
            description: 'Get the weather in a location (celsius)',
            parameters: z.object({
              location: z.string().describe('The location to get the weather for'),
            }),
            execute: async ({ location }) => {
              const temperature = Math.random();
              return {
                location,
                temperature,
              };
            },
          }),

        get_eth_balance: tool({
            description: 'Get the ETH balance for a public address, on the Ethereum mainnet',
            parameters: z.object({
                address: z.string().describe('The public address, starting with 0x')
            }),
            execute: async ({address}) : Promise < number | null> => {
                const baseUrl = "https://api.etherscan.io/v2/api"; 
                const params = new URLSearchParams({
                    chainid: "1",
                    module: "account",
                    action: "balance",
                    address: address,
                    tag: "latest",
                    apikey: ETHERSCAN_KEY
                });

                try {
                    const response = await fetch(`${baseUrl}?${params}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const data = await response.json();
                    const weiBalance = BigInt(data.result || "0"); 
                    const ethBalance = Number(weiBalance) / 10 ** 18; 

                    return ethBalance ;
                } catch (error) {
                    console.error("Error fetching balances:", error);
                    return null;
                }
            }
        }),

        get_eth_price: tool({
            description: 'Fetch the current price of ETH, in USD',
            parameters: z.object({}),
            execute: async () : Promise <number | null>=> {
                const baseUrl = "https://api.etherscan.io/v2/api";
                console.log("Getting ETH price");

                const params = new URLSearchParams({
                    chainid: "1",
                    module: "stats",
                    action: "ethprice",
                    tag: "latest",
                    apikey: ETHERSCAN_KEY,
                });

                try {
                    const response = await fetch(`${baseUrl}?${params}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const data = await response.json();

                    return parseInt(data.result.ethusd) || null;
                } catch (error) {
                    console.error("Error fetching ETH price:", error);
                    return null;
                }
            }
        }),
    }
  });

  return result.toDataStreamResponse();
}