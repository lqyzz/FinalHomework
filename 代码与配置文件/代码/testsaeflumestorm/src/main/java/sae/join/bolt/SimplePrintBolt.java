package sae.join.bolt;


import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;

import java.util.Map;

public class SimplePrintBolt extends BaseRichBolt {
    OutputCollector _collector;

    public void prepare(Map config, TopologyContext context, OutputCollector collector) {
        this._collector = collector;
    }
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    }

    public void execute(Tuple tuple) {
        System.out.println(tuple);
        System.out.println(tuple.getString(0));
        //注意确认ack，对应在flume的配置文件中，如果没有，即使退出zk, flume, kafka，队列中的未处理信息也不会消失
        this._collector.ack(tuple);
    }

}
