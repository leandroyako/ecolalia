(
SynthDef.new(\playbuf, {
	arg amp=1, out=0, pos=0, buf, rate=1, da=2;
	var sig, env;
	env = Env.asr(0.01, BufDur.kr(buf) - 0.02, 0.01).kr(doneAction:da);
	sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf) * rate);
	sig = sig * env;
	sig = Pan2.ar(sig, pos) * amp;
	Out.ar(out, sig);
}).writeDefFile;

~wavs_dir = "agn_bicentenario_wav/";
~word = "nosotros";
File.mkdir(thisProcess.nowExecutingPath.asPathName.pathOnly ++ ~word);
~nosotros = JSONFileReader.read("~/sc/nosotros.json");
)

(
~nosotros.do({	|word|
	var path = ~wavs_dir ++ word["filename"] ++ ".wav";
	var sndfile = SoundFile.openRead(path);
	var startFrame = word["start"].asFloat * sndfile.numChannels * sndfile.sampleRate;
	var duration = word["end"].asFloat - word["start"].asFloat + 0.02;
	var numFrames = duration * sndfile.numChannels * sndfile.sampleRate;
	var outputFilename = [word["filename"], word["start"], word["end"]].join("_") ++ ".wav";
	var outputFilePath = thisProcess.nowExecutingPath.asPathName.pathOnly ++ ~word +/+ outputFilename;

	if(
		File.exists(outputFilePath),
		{
			(outputFilePath ++ " already exists").postln;
		},
		{
			var pattern;
			var buffer = Buffer.new;
			var score = Score.new;
			score.add([0, buffer.allocReadMsg(path, startFrame, numFrames)]);
			pattern = Pbind(\instrument, \playbuf, \buf, buffer);
			pattern = pattern.asScore(duration);
			pattern.score.do{|e| score.add(e)};
			score.recordNRT(
				outputFilePath: outputFilePath,
				headerFormat: "wav",
				sampleFormat: "int32",
				options: ServerOptions.new.numOutputBusChannels_(sndfile.numChannels).numBuffers_(2097152),
				action: { outputFilename.postln }
			)
		}
	);
});
)