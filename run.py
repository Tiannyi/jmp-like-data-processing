#!/usr/bin/env python3
import os
import subprocess
import time
from pathlib import Path

class Runner:
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.frontend_dir = self.root_dir / 'frontend'
        self.backend_dir = self.root_dir / 'backend'
        self.venv_dir = self.root_dir / '.venv'
        self.python = str(self.venv_dir / 'bin' / 'python')
        self.pip = str(self.venv_dir / 'bin' / 'pip')

    def print_step(self, message):
        print(f"\n{'=' * 20}\n{message}\n{'=' * 20}", flush=True)

    def print_progress(self, message):
        print(f">> {message}", flush=True)

    def kill_process_on_port(self, port):
        try:
            # Find process ID using port
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                # Kill the process
                self.print_progress(f"Terminating process on port {port}...")
                subprocess.run(['kill', '-9', result.stdout.strip()])
        except subprocess.CalledProcessError:
            # No process found on port
            pass

    def cleanup(self):
        """Clean up all running processes"""
        self.print_step("Cleaning up processes...")
        self.kill_process_on_port(3000)  # Frontend
        self.kill_process_on_port(8000)  # Backend
        
        # Give processes time to fully terminate
        time.sleep(1)

    def start_backend(self):
        self.print_step("Starting backend server...")
        os.chdir(self.backend_dir)
        
        # Check if virtual environment exists
        if not self.venv_dir.exists():
            print("\nError: Virtual environment not found. Please set it up first:", flush=True)
            print("  python3.11 -m venv .venv", flush=True)
            print("  source .venv/bin/activate", flush=True)
            print("  pip install -r backend/requirements.txt\n", flush=True)
            raise Exception("Virtual environment not found")
        
        # Kill any existing process on port 8000
        self.kill_process_on_port(8000)
        
        self.print_progress("Launching backend server...")
        backend_process = subprocess.Popen(
            [self.python, '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for backend to be ready
        self.print_progress("Waiting for backend to be ready...")
        max_attempts = 10
        for i in range(max_attempts):
            try:
                subprocess.run(['curl', 'http://localhost:8000/health'], 
                             capture_output=True, check=True)
                self.print_progress("Backend is ready!")
                return backend_process
            except subprocess.CalledProcessError:
                if i < max_attempts - 1:
                    self.print_progress(f"Waiting... ({i+1}/{max_attempts})")
                    time.sleep(1)
                else:
                    print("Error: Backend server failed to start", flush=True)
                    backend_process.terminate()
                    raise Exception("Backend server failed to start")

    def start_frontend(self):
        self.print_step("Starting frontend development server...")
        os.chdir(self.frontend_dir)
        
        # Check if node_modules exists
        if not (self.frontend_dir / 'node_modules').exists():
            print("\nError: Frontend dependencies not found. Please install them first:", flush=True)
            print("  cd frontend", flush=True)
            print("  npm install\n", flush=True)
            raise Exception("Frontend dependencies not found")
        
        # Kill any existing process on port 3000
        self.kill_process_on_port(3000)
        
        self.print_progress("Launching frontend server...")
        env = os.environ.copy()
        env['BROWSER'] = 'none'  # Prevent auto-opening browser
        env['FAST_REFRESH'] = 'true'  # Enable fast refresh
        frontend_process = subprocess.Popen(
            ['npm', 'start', '--no-cache'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Wait for frontend to be ready
        self.print_progress("Waiting for frontend to be ready...")
        max_attempts = 20
        for i in range(max_attempts):
            try:
                subprocess.run(['curl', 'http://localhost:3000'], 
                             capture_output=True, check=True)
                self.print_progress("Frontend is ready!")
                return frontend_process
            except subprocess.CalledProcessError:
                if frontend_process.poll() is not None:
                    stdout, stderr = frontend_process.communicate()
                    print("\nFrontend server failed to start. Output:", flush=True)
                    print("\nStdout:", flush=True)
                    print(stdout, flush=True)
                    print("\nStderr:", flush=True)
                    print(stderr, flush=True)
                    raise Exception("Frontend server failed to start")
                if i < max_attempts - 1:
                    self.print_progress(f"Waiting... ({i+1}/{max_attempts})")
                    time.sleep(1)
                else:
                    stdout, stderr = frontend_process.communicate()
                    print("\nFrontend server failed to start. Output:", flush=True)
                    print("\nStdout:", flush=True)
                    print(stdout, flush=True)
                    print("\nStderr:", flush=True)
                    print(stderr, flush=True)
                    frontend_process.terminate()
                    raise Exception("Frontend server failed to start")

    def run(self):
        try:
            backend_process = self.start_backend()
            frontend_process = self.start_frontend()
            
            # Keep the script running
            backend_process.wait()
            frontend_process.wait()
            
        except KeyboardInterrupt:
            self.print_step("Shutting down...")
        except Exception as e:
            print(f"\nError: {str(e)}", flush=True)
        finally:
            self.cleanup()

if __name__ == '__main__':
    try:
        runner = Runner()
        runner.run()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        if 'runner' in locals():
            runner.cleanup()
