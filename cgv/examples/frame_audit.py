import argparse
import os
import json
import sys
from cgv.media import extract_frames, compare_frames, _ensure_parent
from cgv.manifest import ArtifactRegistry
from cgv.schemas import VisualGroundingResult

def main():
    parser = argparse.ArgumentParser(description="Deterministic frame audit example (CGV)")
    parser.add_argument("--input", required=True, help="Path to input video file")
    parser.add_argument("--out", default="runs/demo", help="Output directory")
    parser.add_argument("--ask-vlm", action="store_true", help="Query remote VLM (requires key)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input video not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Step 1: Extracting keyframes from {args.input}...")
    # Extract at 0.5s, 4.0s, 7.6s (or middle depending on duration)
    timestamps = [0.5, 4.0, 7.5]
    try:
        frames = extract_frames(args.input, timestamps, os.path.join(args.out, "frames"))
    except Exception as e:
        print(f"Error extracting frames: {e}", file=sys.stderr)
        sys.exit(1)

    print("Extracted frames:")
    for f in frames:
        print(f"  - {f}")

    print("\nStep 2: Computing pixel difference between frame 0 and frame 1...")
    diff_vis_path = os.path.join(args.out, "diffs", "diff_0_1.jpg")
    try:
        _, diff_percent = compare_frames(frames[0], frames[1], diff_vis_path)
        print(f"  - Pixel difference: {diff_percent:.2f}%")
        print(f"  - Diff visualization saved to: {diff_vis_path}")
    except Exception as e:
        print(f"Error comparing frames: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nStep 3: Registering artifacts in manifest...")
    manifest_path = os.path.join(args.out, "manifest.json")
    registry = ArtifactRegistry(manifest_path)
    
    uris = []
    for i, f in enumerate(frames):
        uri = registry.register(f, label=f"frame_{i}", purpose=f"QC Frame at timestamp {timestamps[i]}s")
        uris.append(uri)
    diff_uri = registry.register(diff_vis_path, label="diff_0_1", purpose="Visual diff between frame 0 and 1")
    
    print(f"Manifest written to {manifest_path} with registered URIs:")
    for u in uris:
        print(f"  - {u}")
    print(f"  - {diff_uri}")

    # Step 4: VLM step
    if args.ask_vlm:
        print("\nStep 4: Querying remote VLM...")
        provider = os.getenv("CGV_VLM_PROVIDER")
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        if not provider or not api_key:
            print("Error: CGV_VLM_PROVIDER and appropriate API key must be set for --ask-vlm.", file=sys.stderr)
            sys.exit(1)
            
        print(f"  - Using provider: {provider}")
        print("  - VLM call simulation: schema validation check.")
        # In a real environment, this invokes the VLM client. For demo, we compile a mockup complying with the schema:
        mock_result = VisualGroundingResult(
            answer=True,
            evidence=f"Pixel diff between frame 0 and 1 is {diff_percent:.2f}%. Both frames show correct chrysalis bodice.",
            confidence=0.95,
            needs_deterministic_check=False,
            regions=[]
        )
        print("VLM Result parsed against schema:")
        print(mock_result.model_dump_json(indent=2))
    else:
        print("\nPrompt instructions generated (copy-paste to your VLM):")
        print("--------------------------------------------------")
        print(f"Please inspect the frames registered in the manifest: {manifest_path}")
        print(f"Images to read: {', '.join(frames)}")
        print("Is the visual continuity maintained between these frames? Answer in JSON schema format.")
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()
