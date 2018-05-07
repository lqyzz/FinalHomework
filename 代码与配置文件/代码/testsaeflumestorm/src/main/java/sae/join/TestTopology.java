package sae.join;


import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.spout.SchemeAsMultiScheme;
import backtype.storm.topology.TopologyBuilder;
import sae.join.bolt.SimplePrintBolt;
import storm.kafka.*;

import java.util.Arrays;

public class TestTopology {

    public static void main(String[] args) throws Exception {
        //String zks = "localhost:2181";
        //String zkRoot = "/home/sae/software/zookeeper";
        String zks = "lx-svr-1:2181";
        String zkRoot = "/home/software/zookeeper";

        String topic = "flume-kafka";
        String id = "kafka-data";

        BrokerHosts brokerHosts = new ZkHosts(zks);
        SpoutConfig spoutConf = new SpoutConfig(brokerHosts, topic, zkRoot, id);
        spoutConf.scheme = new SchemeAsMultiScheme(new StringScheme());
        spoutConf.zkServers = Arrays.asList(new String[] {"lx-svr-1"});
        spoutConf.zkPort = 2181;


        TopologyBuilder builder = new TopologyBuilder();
        builder.setSpout("kafka-reader", new KafkaSpout(spoutConf), 3);
        builder.setBolt("simple-print", new SimplePrintBolt(), 3)
                .shuffleGrouping("kafka-reader");


        Config config = new Config();
        config.setDebug(true);

        if (args != null && args.length > 0) {
            config.setNumWorkers(3);
            StormSubmitter.submitTopology(args[0], config, builder.createTopology());
        } else {
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("test-topology", config, builder.createTopology());
        }


    }
}
