# if __name__ == "__main__":
#     from arcadefire.main import main
#     main()


import argparse
from arcadefire.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the arcadefire game.")
    parser.add_argument('--profile', action='store_true',
                        help='enable profiling of the update function')

    args = parser.parse_args()
    
    # Pass the parsed args to the main function
    main(profile=args.profile)
