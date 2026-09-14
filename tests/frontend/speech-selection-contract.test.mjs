import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const source = await readFile(new URL('../../src/dashboard/static/speech-reader.js', import.meta.url), 'utf8');
const speech = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);

function voicesFixture(voices) {
  globalThis.window = {
    speechSynthesis: { getVoices: () => voices },
    SpeechSynthesisUtterance: class {},
  };
  globalThis.localStorage = { getItem: () => null };
}

test('natural Microsoft voices are preferred within the requested language', () => {
  const ordinary = { name: 'Desktop Standard', lang: 'de-DE', default: true, localService: true };
  const natural = { name: 'Microsoft Katja Online (Natural)', lang: 'de-DE', localService: false };
  const english = { name: 'Microsoft Jenny Online (Natural)', lang: 'en-US' };
  voicesFixture([ordinary, english, natural]);
  assert.equal(speech.chooseSpeechVoice('de-DE'), natural);
  assert.equal(speech.chooseSpeechVoice('en-US'), english);
});

test('explicit voice selection is preserved rather than overwritten by ranking', () => {
  const katja = { name: 'Microsoft Katja Online (Natural)', lang: 'de-DE' };
  const conrad = { name: 'Microsoft Conrad', lang: 'de-DE' };
  voicesFixture([katja, conrad]);
  assert.equal(speech.chooseSpeechVoice('de-DE', conrad.name), conrad);
});

test('late voice availability is read afresh and missing voices are not invented', () => {
  const voices = [];
  voicesFixture(voices);
  assert.equal(speech.chooseSpeechVoice('de-DE'), null);
  const voice = { name: 'Microsoft Katja Online (Natural)', lang: 'de-DE' };
  voices.push(voice);
  assert.equal(speech.chooseSpeechVoice('de-DE'), voice);
  assert.equal(speech.chooseSpeechVoice('en-US'), null);
});
