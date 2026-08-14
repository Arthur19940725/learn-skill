# Source-Grounding Fixtures

Synthetic excerpts for deterministic skill evaluations. These are test data, not summaries of real publications.

## Empirical paper: Market Signaling Study

[P1] The study asks whether buyers lower their offers when product quality is known only to sellers. It predicts that information asymmetry can push high-quality sellers out of a market.

[P2] Researchers compare offers in two controlled market rounds. In round A, buyers observe verified quality labels. In round B, only sellers observe quality. Median offers and completed trades are recorded for each round.

[P3] Round B produces lower median offers and fewer high-quality trades than round A. The authors state that this pattern is consistent with adverse selection, but the small laboratory sample limits generalization to large online markets.

[P4] The authors propose verified warranties as one possible signal. They do not test warranty design, enforcement cost, or long-run seller behavior.

## Conceptual chapter: Reliable Queue Consumers

[C1] The chapter's purpose is to explain how a queue consumer can process messages at least once without silently losing work.

[C2] Core requirements are durable acknowledgement, idempotent handling, bounded retries, and a dead-letter path. Acknowledgement must occur only after the business side effect succeeds.

[C3] The mechanism is a receive-process-acknowledge loop. Duplicate delivery is expected, so the handler stores a stable operation key before applying a non-repeatable side effect.

[C4] The chapter gives a payment-webhook example. It does not specify a vendor SDK, exact retry delays, or a globally correct deduplication store.

## Incident report: Checkout Latency Event

[R1] Scope: checkout requests in region west between 09:10 and 09:42 UTC. Median latency rose from 220 ms to 4.8 s.

[R2] Evidence: database connection-pool wait time rose first, followed by API timeout count. CPU and memory remained within normal ranges.

[R3] Causal analysis: a deployment reduced pool size while traffic stayed constant. Rolling back the configuration restored wait time within six minutes.

[R4] Uncertainty and action: the report cannot determine why pre-deploy load testing missed the queueing effect. Actions are to add pool-wait alerts, a concurrency regression test, and a deployment guardrail.
