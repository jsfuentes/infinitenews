# Notebooks to run forced alignment on characters. 

The "forced_alignment.ipynb" has the main alignment function, with an example call.

The main function is called `run_forced_alignment`. It takes three arguments:
- Name of the wav2vec2 model (default: "WAV2VEC2_ASR_LARGE_LV60K_960H")
- Path to wav file with audio.  
- Path to the text file with the transcript. Can also be a string with the transcript itself. 


The function returns a dictionary with two objects:
- `character_segs`: Gives frame-level alignments for each character.
- `word_segs`: Gives frame-level alignments for each word. 



NOTE: The "forced_alignment_annotated.ipynb" notebook has a lot of plots and visualizations to check the output.

