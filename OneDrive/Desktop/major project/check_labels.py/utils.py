import pefile
import numpy as np
import hashlib

def extract_features(file_path):
    try:
        pe = pefile.PE(file_path)

        features = {}

        # 1. File Hash Feature
        with open(file_path, "rb") as f:
            data = f.read()
        features["sha256"] = int(hashlib.sha256(data).hexdigest(), 16) % (10**8)

        # 2. General file info
        features["size"] = len(data)
        features["num_sections"] = len(pe.sections)
        features["entrypoint"] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        features["imagebase"] = pe.OPTIONAL_HEADER.ImageBase

        # 3. Section features
        entropy_list = []
        sizes_list = []

        for section in pe.sections:
            sizes_list.append(section.SizeOfRawData)
            entropy_list.append(section.get_entropy())

        # Fixed length (pad or truncate to 10 sections)
        sizes_list = (sizes_list + [0]*10)[:10]
        entropy_list = (entropy_list + [0]*10)[:10]

        for i in range(10):
            features[f"sec_size_{i}"] = sizes_list[i]
            features[f"sec_entropy_{i}"] = entropy_list[i]

        # 4. Import count
        try:
            features["imports"] = sum([len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT])
        except:
            features["imports"] = 0

        # 5. Export count
        try:
            features["exports"] = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
        except:
            features["exports"] = 0

        # 6. Characteristics
        features["characteristics"] = pe.FILE_HEADER.Characteristics

        # Return in sorted order for ML
        return np.array(list(features.values()), dtype=float)

    except Exception as e:
        print("Failed to parse PE:", file_path, "Error:", e)
        return None
