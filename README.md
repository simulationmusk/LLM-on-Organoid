# LLM on Organoids

## Brain in a Vat: A Hybrid Neural-Digital Consciousness Experiment

## Overview

This project presents the first practical implementation of Hilary Putnam's "Brain in a Vat" thought experiment, creating a basic unconscious simulation based on real human behavioral data. We've built a hybrid system combining:

1. **Biological Component**: FinalSpark's living brain cell (Organoid) for modeling subconsciousness
2. **Digital Component**: A fine-tuned Large Language Model (Llama 3.3 70B) for modeling consciousness

The system uses Elon Musk's 50,890 tweets accumulated over 15 years to replicate his personality patterns, creating a simulated consciousness that bridges artificial intelligence with living neural networks.

## Project Architecture

![Organoid System](Figures/Scheme.png)

### Two-System Architecture

#### 1. Consciousness: Linguistic Intelligence
- **Model**: Llama 3.3 70B
- **Method**: LoRA fine-tuning
- **Training Data**: 50,890 tweets from Elon Musk's timeline (2010-2025)
- **Function**: Handles complex language processing and conscious decision-making

#### 2. Subconsciousness: Neural Organoid System
- **Composition**: Four living brain organoids from FinalSpark
- **Size**: Approximately 500 micrometers each
- **Interface**: 32 specialized electrodes for bi-directional communication
- **Function**: Processes emotional, linguistic, memory, and attention patterns

![Organoid System](Figures/organoid_single.png)

![Organoid System](Figures/organoid_system.png)

## Technical Components

### Organoid System
The biological computing core consists of human stem cell-derived mini-brains that:
- Receive electrical stimuli converted from textual content
- Generate unique neural response patterns
- Form memories through repeated stimulation
- Influence the LLM's response generation

### LLM Persona
- **Base Model**: Llama 3.3 70B
- **Fine-tuning**: Custom LoRA weights
- **Training Corpus**:
  - 12,533 tweets (2010-2021)
  - 38,357 tweets (2021-2025)
- **Response Generation**: Contextually aware with organoid feedback integration

## How It Works

1. **Tweet Processing**: Incoming tweets from X are analyzed for emotional content, linguistic complexity, context/memory patterns, and attention-grabbing features.
2. **Neural Stimulation**: Each tweet generates a unique pattern of electrical signals sent to the subconsciousness system consisting of four organoids (each serving as Emotional, Linguistic, Memory, and Attension units).
3. **Organoid Response**: The organoid system constantly fire electric signals but generates large peaks upon triggers. These activity patterns are measured across channels, monitored through 8 electrodes per organoid.
4. **Hybrid Response Generation**: The LLM generates responses influenced by both the tweet content and the organoid activity. The LLM-Organoid-generated tweets are then posted on X automatically.

## Installation & Setup

### Prerequisites
- Python 3.8+
- FinalSpark Neuroplatform access
- Intan RHX system
- Fine-tuned Llama 3.3 70B model


### Configuration
1. Set up your Twitter API credentials in `src/config.py`
2. Configure organoid connection parameters
3. Initialize the system:
```python
from src.organoid import OrganoidSystem
system = OrganoidSystem()
await system.initialize_system()
```

## Usage

Basic tweet processing:
```python
# Process a single tweet
tweet = "Your tweet text here"
trigger_values = system.compute_tweet_triggers(tweet)
await system.send_triggers(trigger_values)
organoid_response = await system.get_organoid_status(seconds=5)
response = generator.generate_response_with_timeout(tweet, organoid_response=organoid_response)
```

## Research Applications

This system enables exploration of:
- Biological-digital hybrid computing
- Neural response patterns to linguistic stimuli
- Unconscious behavior simulation
- Pattern learning in organoid systems

## Ethical Considerations

This project raises important questions about consciousness simulation and the boundaries between biological and digital computation. All organoid work follows established ethical guidelines for neural tissue research.


## License

This project is licensed under [NC-SA 4.0] - see the LICENSE file for details.

## Acknowledgments

- Meta for providing Llama 3.3 70B LLM
- FinalSpark (https://finalspark.com) for providing the Neuroplatform technology
