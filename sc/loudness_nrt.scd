(
s.options.numBuffers_(2097152);
s.boot;

SynthDef.new(\playbuf, {
	arg amp=1, out=0, pos=0, buf, rate=1, da=2;
	var sig, env;
	env = Env.asr(0.01, BufDur.kr(buf) - 0.02, 0.01).kr(doneAction:da);
	sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf) * rate);
	sig = sig * env;
	sig = Pan2.ar(sig, pos) * amp;
	Out.ar(out, sig);
}).writeDefFile;

~wavs_dir = "~/sc/nosotros_normalized";
~words = JSONFileReader.read("~/sc/loudness.json");
)

(
~soundfiles = SoundFile.collect(~wavs_dir+/+"*").do { |f|
	f.duration.postln };
~soundfiles.sort({ |a, b| a.duration > b.duration});

~deltaEnv = Env.xyc([[0,0,2],[0.7, ~soundfiles[1].duration*0.7],[1.0, ~soundfiles[1].duration*0.8]]);
~delta = ~words.size.collect({ |i|
	var index = ~deltaEnv.duration/i;
	index.postln;
	~deltaEnv.at(index)
});
~delta = ~delta.reverse;

~score = Score.new;

~loudnessBuf = ~words.collect({ |word|
	var path = ~wavs_dir +/+ word["filename"];
	var buffer = Buffer.new;
	~score.add([0, buffer.allocReadMsg(path) ]);
	buffer;
});

~pattern = Pbind(
	\instrument, \playbuf,
	\buf, Pseq(~loudnessBuf),
	\amp, 0.7,
	\delta, Pwhite(0.01, 0.1) + Pseq(~delta),
	\finish, Pfunc({|e| e.buf.postln})
);

~pattern = ~pattern.asScore(250);
~pattern.score.do{|e| ~score.add(e)};

~outFile = thisProcess.nowExecutingPath.asPathName.pathOnly ++ "loudness_nrt_exp.wav";

~score.recordNRT(
	outputFilePath: ~outFile.asAbsolutePath,
	headerFormat: "wav",
	sampleFormat: "int32",
	options: ServerOptions.new.numOutputBusChannels_(2).numBuffers_(2097152).maxNodes_(32768).memSize_(2 ** 21),
	action: { "done".postln }
);
)
