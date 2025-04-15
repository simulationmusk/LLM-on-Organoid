from datetime import timedelta, datetime, timezone
import numpy as np
import time
from neuroplatformv2.core.trigger import TriggerController
from neuroplatformv2.core.database import (
    DatabaseController,
    TriggersQuery,
    SpikeCountQuery,
    SpikeEventQuery,
    RawSpikeQuery,
    get_raw_spike,
)
from neuroplatformv2.core.intan import IntanController
from neuroplatformv2.utils.schemas import (
    StimParam,
    StimPolarity,
    StartRawRecordingRequest,
)


import asyncio
import nest_asyncio
import re
from transformers import pipeline
import numpy as np
from neuroplatformv2.core.trigger import TriggerController
from neuroplatformv2.core.intan import IntanController
from neuroplatformv2.utils.schemas import StimParam, StimPolarity
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob
import time
import random




class OrganoidProcessor:
    """Base class for specialized organoid processors"""
    def __init__(self, organoid_index):
        self.organoid_index = organoid_index
        self.stim_param = None

    def process(self, tweet):
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process method")





class EmotionalOrganoid(OrganoidProcessor):
    """Organoid 1: Processes emotional content"""
    def __init__(self):
        super().__init__(0)
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def process(self, tweet):
        # Analyze emotional valence and intensity
        sentiment = self.sentiment_analyzer(tweet)[0]
        # Create combined score (-1 to 1) * confidence
        score = (1 if sentiment['label'] == 'POSITIVE' else -1) * sentiment['score']
        return score

class LinguisticOrganoid(OrganoidProcessor):
    """Organoid 2: Processes linguistic complexity"""
    def __init__(self):
        super().__init__(1)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)

    def process(self, tweet):
        # Analyze linguistic complexity
        sentences = sent_tokenize(tweet)
        words = word_tokenize(tweet)
        unique_words = set(words)

        # Calculate complexity score based on:
        # - Vocabulary diversity (type-token ratio)
        # - Average sentence length
        # - Word length
        type_token_ratio = len(unique_words) / len(words)
        avg_sent_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)

        # Normalize score to -1 to 1 range
        complexity_score = (type_token_ratio +
                          (avg_sent_length / 20) +  # normalize by typical max
                          (avg_word_length / 10)) / 3  # normalize by typical max
        return min(max(complexity_score, -1), 1)  # clamp to [-1, 1]

class MemoryOrganoid(OrganoidProcessor):
    """Organoid 3: Processes contextual/memory patterns"""
    def __init__(self):
        super().__init__(2)
        self.context_memory = []  # Could be expanded to persist between tweets

    def process(self, tweet):
        # Look for patterns, repetitions, and references
        words = word_tokenize(tweet.lower())

        # Count hashtags, mentions, and urls as context markers
        context_markers = len(re.findall(r'#\w+|@\w+|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet))

        # Count repeated words
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        repetitions = sum(count - 1 for count in word_counts.values())

        # Create normalized score based on context and repetition
        score = (context_markers + repetitions) / (len(words) + 1)  # +1 to avoid division by zero
        return min(max(score * 2 - 1, -1), 1)  # normalize to [-1, 1]

class AttentionOrganoid(OrganoidProcessor):
    """Organoid 4: Processes attention-grabbing features"""
    def __init__(self):
        super().__init__(3)

    def process(self, tweet):
        # Analyze attention-grabbing features:
        # - Exclamation marks
        # - ALL CAPS words
        # - Emoji presence
        # - Question marks
        exclamation_count = tweet.count('!')
        question_count = tweet.count('?')
        caps_words = sum(1 for word in tweet.split() if word.isupper() and len(word) > 1)
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', tweet))

        # Calculate attention score
        total_weight = 4  # number of features
        attention_score = (
            (exclamation_count / 3) +  # normalize by typical max
            (question_count / 3) +
            (caps_words / 3) +
            (emoji_count / 3)
        ) / total_weight

        return min(max(attention_score * 2 - 1, -1), 1)  # normalize to [-1, 1]




class OrganoidSystem:
    def __init__(self):
        # Initialize organoid processors
        self.organoids = [
            EmotionalOrganoid(),
            LinguisticOrganoid(),
            MemoryOrganoid(),
            AttentionOrganoid()
        ]

        # Initialize controllers
        self.intan = IntanController()
        self.trigger = TriggerController("admin")

        # Define electrode mapping
        self.electrode_mapping = {
            0: {'method': 'bernoulli', 'electrodes': list(range(8))},
            1: {'method': 'bernoulli', 'electrodes': list(range(8))},
            2: {'method': 'bernoulli', 'electrodes': list(range(8))},
            3: {'method': 'bernoulli', 'electrodes': list(range(8))}
        }

        # Flag to track initialization
        self.is_initialized = False

    def create_standard_stim_params(self):
        """
        Create a standard set of 16 stimulation parameters,
        each targeting a unique electrode in the 0-31 range
        """
        stim_params = []
        for i in range(16):
            stim_param = StimParam()
            stim_param.enable = True

            # Distribute electrodes across the 0-31 range
            linear_electrode_index = i * 2  # This ensures we use different electrodes

            stim_param.index = linear_electrode_index
            stim_param.trigger_key = i
            stim_param.polarity = StimPolarity.PositiveFirst

            # Default parameters
            stim_param.phase_duration1 = 100
            stim_param.phase_duration2 = 100
            stim_param.phase_amplitude1 = 0.5
            stim_param.phase_amplitude2 = 0.5

            stim_params.append(stim_param)

        return stim_params

    async def initialize_system(self):
        """
        Pre-upload the standard stimulation parameters
        """
        if self.is_initialized:
            print("System already initialized")
            return True

        # Create standard stim params
        standard_stim_params = self.create_standard_stim_params()

        # Send standard stimulation parameters
        resp = await self.intan._send_stimparam(standard_stim_params)
        if not resp.status:
            print(f"Error updating standard stim parameters: {resp.message}")
            return False

        # Upload standard stim parameters
        resp = await self.intan._upload_stimparam()
        if not resp.status:
            print(f"Error uploading standard stim parameters: {resp.message}")
            return False

        # Mark as initialized
        self.is_initialized = True
        print("System initialized successfully")
        return True

    def _bernoulli_electrode_selection(self, p=0.4, max_electrodes=5):
        """
        Select electrodes using i.i.d. Bernoulli sampling

        Args:
        p (float): Probability of selecting each electrode (default 0.4)
        max_electrodes (int): Maximum number of electrodes to select (default 4)

        Returns:
        list: Indices of selected electrodes
        """
        # For each organoid, use 8 electrodes
        electrodes = list(range(8))

        # Use Bernoulli sampling to select electrodes
        selected_electrodes = [
            electrode for electrode in electrodes
            if random.random() < p
        ]

        # Truncate to max_electrodes if necessary
        if len(selected_electrodes) > max_electrodes:
            selected_electrodes = random.sample(selected_electrodes, max_electrodes)

        # Ensure at least one electrode is selected
        if not selected_electrodes:
            selected_electrodes = [random.choice(electrodes)]

        return selected_electrodes


    def compute_tweet_triggers(self, tweet_text):
        """
        Compute triggers for a tweet without sending them
        Returns a numpy array of trigger values
        """
        # Prepare trigger values
        trigger_values = np.zeros(16, dtype=np.uint8)

        # Process each organoid
        for organoid_index, organoid in enumerate(self.organoids):
            value = organoid.process(tweet_text)  # from -1 to 1
            prob_electrode = (value + 1) / 4  # probability of selecting each electrode: 0 to 1/2

            # Select active electrodes
            active_electrodes = self._bernoulli_electrode_selection(p=prob_electrode)

            # Activate corresponding triggers based on active electrodes
            for electrode in active_electrodes:
                # Calculate the trigger key for this organoid's electrode
                trigger_key = organoid_index * 8 + electrode

                if 0 <= trigger_key < 16:
                    trigger_values[trigger_key] = 1

            # Print organoid input
            organoid_types = ["Emotional", "Linguistic", "Memory", "Attention"]
            print(f"{organoid_types[organoid_index]} Organoid input: {value:.3f}, Active Electrodes: {active_electrodes}")

        return trigger_values

    async def send_triggers(self, trigger_values):
        """
        Send the computed triggers one by one
        """
        for i in np.arange(16):
            if trigger_values[i]==1:
                triggers = np.zeros(16, dtype=np.uint8)
                triggers[i] = 1
                await self.trigger.send(triggers)
                time.sleep(0.5)


    async def get_organoid_status(self, seconds=5):
        """Analyze recent organoid activity and return a context summary"""
        now = datetime.now(timezone.utc)
        activity_summary = {
            'total_spikes': 0,
            'active_channels': 0,
            'max_amplitude': 0,
            'organoid_states': []
        }

        for organoid in range(4):
            organoid_activity = 0
            active_channels = 0
            max_amp = 0

            for channel in range(8):
                channel_idx = organoid * 8 + channel
                query = RawSpikeQuery(
                    start=now - timedelta(seconds=seconds),
                    stop=now,
                    index=channel_idx
                )

                try:
                    df = await DatabaseController.get_raw_spike(query)
                    if len(df) > 0:
                        active_channels += 1
                        organoid_activity += len(df)
                        max_amp = max(max_amp, df['Amplitude'].max())
                except Exception as e:
                    continue

            activity_summary['organoid_states'].append({
                'id': organoid + 1,
                'activity_level': 'high' if organoid_activity > 1000 else 'medium' if organoid_activity > 100 else 'low',
                'active_channels': active_channels,
                'max_amplitude': max_amp
            })

            activity_summary['total_spikes'] += organoid_activity
            activity_summary['active_channels'] += active_channels
            activity_summary['max_amplitude'] = max(activity_summary['max_amplitude'], max_amp)

        return activity_summary
