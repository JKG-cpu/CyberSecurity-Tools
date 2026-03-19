import bcrypt
import hashlib
import random

from src import *

class Test:
    def __init__(self) -> None:
        self.hashes = {
            "SHA256": hashlib.sha256(b'This is a test hash').hexdigest(),
            "SHA1":   hashlib.sha1(b'This is a test hash').hexdigest(),
            "MD5":    hashlib.md5(b'This is a test hash').hexdigest(),
            "bcrypt": bcrypt.hashpw(b'This is a test hash', bcrypt.gensalt(rounds=4)).decode()
        }

    def run_test(self, iterations: int = 100) -> None:
        types = list(self.hashes.keys())
        results = []
        passed = 0
        failed = 0

        for i in range(iterations):
            choice = random.choice(types)
            identified = identify_hash(self.hashes[choice])
            success = identified == choice
            results.append((choice, identified, success))

            if success:
                passed += 1
            else:
                failed += 1

        # Print results
        print(f"{'#':<5} {'Expected':<10} {'Got':<10} {'Result'}")
        print("-" * 40)

        for i, (expected, got, success) in enumerate(results):
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{i+1:<5} {expected:<10} {got:<10} {status}")

        # Summary
        print("-" * 40)
        print(f"Passed: {passed}/{iterations}")
        print(f"Failed: {failed}/{iterations}")

        if failed == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ {failed} test(s) failed — check identify_hash()")


if __name__ == "__main__":
    Test().run_test(iterations=100)
