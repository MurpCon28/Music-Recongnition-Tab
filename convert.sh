{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "baa459f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/bin/bash\n",
    "\n",
    "ext=\".wav\"\n",
    "\n",
    "for i in ./Songs_mp3/*; do\n",
    "\tffmpeg -i \"${i}\" ./Songs_Wav/\"${i:12:-4}\".wav\n",
    "done"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
