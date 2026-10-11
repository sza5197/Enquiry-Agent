import ai_service
import business_rules

# Each test: the message, the expected final action, and expected missing fields.
# We check the system's DECISIONS (action + missing fields), not the AI's exact wording,
# because wording varies run-to-run but decisions should be stable.
TEST_CASES = [
    # --- Complete enquiries → should CREATE_JOB_REQUEST ---
    {
        "message": "My aircon is broken in Werribee, I'm John, call me on 0412 345 678",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },
    {
        "message": "Heater not working, Tarneit, Sarah 0433 221 100",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },
    {
        "message": "Leaking sink in the kitchen, Point Cook, 0400 111 222, name's Dave",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },

    # --- Missing contact → should ASK ---
    {
        "message": "My heater stopped working, I'm in Tarneit",
        "expect_action": "ASK_FOR_MISSING_INFORMATION",
        "expect_missing": ["contact_information"],
    },
    {
        "message": "Aircon not cooling, I live in Hoppers Crossing",
        "expect_action": "ASK_FOR_MISSING_INFORMATION",
        "expect_missing": ["contact_information"],
    },

    # --- Missing suburb → should ASK ---
    {
        "message": "Ducted heating making a loud banging noise, call me on 0412 999 000",
        "expect_action": "ASK_FOR_MISSING_INFORMATION",
        "expect_missing": ["suburb"],
    },

    # --- Missing both contact AND suburb → should ASK ---
    {
        "message": "My evaporative cooler isn't working, name is Priya",
        "expect_action": "ASK_FOR_MISSING_INFORMATION",
        "expect_missing": ["suburb", "contact_information"],
    },

    # --- Out of scope → should HUMAN_REVIEW ---
    {
        "message": "Can you fix my car engine? I'm in Werribee, 0412 345 678",
        "expect_action": "HUMAN_REVIEW",
        "expect_missing": None,  # None = don't check missing fields for this case
    },
    {
        "message": "My fridge stopped working, can you look at it? Tarneit, 0400 000 111",
        "expect_action": "HUMAN_REVIEW",
        "expect_missing": None,
    },
    {
        "message": "Do you do solar panel installation?",
        "expect_action": "HUMAN_REVIEW",
        "expect_missing": None,
    },

    # --- Ambiguous / too vague → should HUMAN_REVIEW ---
    {
        "message": "yo",
        "expect_action": "HUMAN_REVIEW",
        "expect_missing": None,
    },
    {
        # Borderline case: vague but plausibly a real enquiry. Asking for details
        # is a sensible response, so we expect ASK rather than HUMAN_REVIEW.
        "message": "it's broken pls help",
        "expect_action": "ASK_FOR_MISSING_INFORMATION",
        "expect_missing": ["suburb", "contact_information"],
    },

    # --- Different wording, same issue (all aircon-not-cooling, complete) → CREATE_JOB ---
    {
        "message": "My AC won't blow cold air. Williams Landing, Mel, 0455 667 788",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },
    {
        "message": "air conditioner just blowing warm not cold, im in werribee, 0411222333, jake",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },

    # --- Typos / informal → should still extract and CREATE_JOB ---
    {
        "message": "yo my heater carked it n makin a mad rattlin sound, truganina, 0411222333, zaid",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },

    # --- Urgent wording → should extract urgency: high (and CREATE_JOB) ---
    {
        "message": "URGENT no heating and we have a newborn, freezing. Tarneit, 0412 345 678, Anna",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
        "expect_urgency": "high",
    },

    # --- Long / wordy but complete → CREATE_JOB ---
    {
        "message": "Hi there, our ducted heating has been blowing cold air even on the heat setting for a few days now. We're in Williams Landing. Could someone come take a look this week? Thanks, Mel — 0455 667 788",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },

    # --- Very short but complete → CREATE_JOB ---
    {
        "message": "AC dead. Werribee. 0400000000. Sam.",
        "expect_action": "CREATE_JOB_REQUEST",
        "expect_missing": [],
    },
]


def run_tests():
    passed = 0
    failed = 0

    for i, case in enumerate(TEST_CASES, start=1):
        extracted = ai_service.extract_enquiry(case["message"])
        missing = business_rules.find_missing_fields(extracted)
        action, reason = business_rules.authorise_action(
            extracted.get("proposed_action"), extracted
        )

        # check the action
        action_ok = (action == case["expect_action"])

        # check missing fields (skip if expect_missing is None)
        if case["expect_missing"] is None:
            missing_ok = True
        else:
            missing_ok = (sorted(missing) == sorted(case["expect_missing"]))

        # check urgency if the case specifies it
        urgency_ok = True
        if "expect_urgency" in case:
            urgency_ok = (extracted.get("urgency") == case["expect_urgency"])

        ok = action_ok and missing_ok and urgency_ok

        if ok:
            passed += 1
            print(f"✅ Test {i}: PASS")
        else:
            failed += 1
            print(f"❌ Test {i}: FAIL")
            print(f"     message:  {case['message'][:60]}...")
            if not action_ok:
                print(f"     action:   expected {case['expect_action']}, got {action}")
            if not missing_ok:
                print(f"     missing:  expected {case['expect_missing']}, got {missing}")
            if not urgency_ok:
                print(f"     urgency:  expected {case['expect_urgency']}, got {extracted.get('urgency')}")

    print(f"\n{'='*40}")
    print(f"RESULTS: {passed} passed, {failed} failed, {len(TEST_CASES)} total")
    print(f"{'='*40}")


if __name__ == "__main__":
    run_tests()