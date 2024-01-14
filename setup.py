from setuptools import setup, find_packages

setup(
    name='transcribe-live',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'whisper',
        'sounddevice',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'transcribe=src.main:main',
        ],
    },
    # Additional metadata
    description='A live transcription tool using OpenAI Whisper.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/transcribe',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)