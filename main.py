#!/usr/bin/env python3
"""
Weather Data Shipper - Multi-Source Data Polling and Shipping Application

A command-line application that continuously polls weather data from multiple sources,
transforms it to a unified format, and ships it to Logz.io.
"""

import time
import signal
import sys
from typing import List, Dict, Any

from src.config_loader import load_config
from src.data_sources import fetch_all_sources_data
from src.transformers.weather_transformer import transform_weather_data
from src.shipper.logz_io_client import ship_with_retry

class WeatherDataShipper:
    """Main weather data shipper application."""
    
    def __init__(self):
        self.running = True
        self.config = None
        self.pending_data = []
        
    def load_configuration(self):
        """Load application configuration."""
        try:
            self.config = load_config()
            print("✅ Configuration loaded successfully")
            
            polling_interval = self.config.get('polling_interval', 60)
            data_sources_count = len(self.config.get('data_sources', []))
            
            print(f"⏰ Polling interval: {polling_interval} seconds")
            print(f"📊 Data sources configured: {data_sources_count}")
            
        except Exception as e:
            print(f"❌ Failed to load configuration: {e}")
            sys.exit(1)
    
    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        print("🛡️  Signal handlers set up (Ctrl+C for graceful shutdown)")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
        self.running = False
    
    def polling_cycle(self):
        """Execute one complete polling cycle: fetch -> transform -> ship."""
        try:
            print(f"\n🔄 Starting polling cycle at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Step 1: Fetch raw data from all sources
            raw_data = fetch_all_sources_data(self.config)
            
            if not raw_data:
                print("ℹ️  No data fetched this cycle")
                return True
            
            # Step 2: Transform to unified format
            transformed_data = transform_weather_data(raw_data)
            
            if not transformed_data:
                print("⚠️  No valid data after transformation")
                return True
            
            print(f"📋 Transformed {len(transformed_data)} records")
            
            # Step 3: Ship to Logz.io
            success = ship_with_retry(transformed_data, self.config)
            
            if success:
                print("✅ Polling cycle completed successfully")
                return True
            else:
                # Store failed data for retry on shutdown
                self.pending_data.extend(transformed_data)
                print("⚠️  Shipping failed, data stored for retry")
                return False
                
        except Exception as e:
            print(f"❌ Error in polling cycle: {e}")
            return False
    
    def graceful_shutdown(self):
        """Attempt to send any pending data before shutdown."""
        print("\n🔄 Attempting graceful shutdown...")
        
        if self.pending_data:
            print(f"📤 Attempting to send {len(self.pending_data)} pending records...")
            
            shutdown_timeout = self.config.get('application', {}).get('shutdown_timeout', 30)
            
            # Try to send pending data with timeout
            try:
                success = ship_with_retry(self.pending_data, self.config)
                if success:
                    print("✅ Pending data sent successfully")
                else:
                    print("⚠️  Could not send pending data")
                    
                    # Save to file if configured
                    if self.config.get('application', {}).get('persist_on_shutdown', False):
                        self.save_pending_data()
                        
            except Exception as e:
                print(f"❌ Error during graceful shutdown: {e}")
                if self.config.get('application', {}).get('persist_on_shutdown', False):
                    self.save_pending_data()
        
        print("👋 Shutdown complete")
    
    def save_pending_data(self):
        """Save pending data to recovery file."""
        try:
            recovery_file = self.config.get('application', {}).get('recovery_file', './unsent_data.jsonl')
            
            import json
            with open(recovery_file, 'w') as f:
                for record in self.pending_data:
                    f.write(json.dumps(record) + '\n')
            
            print(f"💾 Saved {len(self.pending_data)} records to {recovery_file}")
            
        except Exception as e:
            print(f"❌ Failed to save pending data: {e}")
    
    def run(self):
        """Main application loop."""
        print("🚀 Starting Weather Data Shipper")
        print("=" * 50)
        
        # Load configuration
        self.load_configuration()
        
        # Set up signal handlers
        self.setup_signal_handlers()
        
        polling_interval = self.config.get('polling_interval', 60)
        
        print(f"\n▶️  Starting continuous polling (every {polling_interval}s)")
        print("Press Ctrl+C to stop gracefully")
        
        # Main polling loop
        while self.running:
            try:
                # Execute polling cycle
                self.polling_cycle()
                
                # Wait for next cycle (but check for shutdown signal)
                for _ in range(polling_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                # This shouldn't happen due to signal handler, but just in case
                self.running = False
                break
            except Exception as e:
                print(f"❌ Unexpected error in main loop: {e}")
                # Continue running unless it's a critical error
                time.sleep(5)
        
        # Graceful shutdown
        self.graceful_shutdown()

def main():
    """Entry point for the command-line application."""
    shipper = WeatherDataShipper()
    shipper.run()

if __name__ == "__main__":
    main()