import torch

def test_gpu() -> bool:
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"CUDA is available. Using device: {torch.cuda.get_device_name(device)}")
        return True
    else:
        print("CUDA is not available. Using CPU.")
        return False

def main():
    test_gpu()

if __name__ == "__main__":
    main()
