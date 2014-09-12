/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package monasca.thresh;

import static org.mockito.Mockito.mock;

import com.hpcloud.mon.common.event.AlarmDefinitionCreatedEvent;
import com.hpcloud.mon.common.event.AlarmDefinitionDeletedEvent;
import com.hpcloud.mon.common.model.alarm.AlarmExpression;
import com.hpcloud.mon.common.model.alarm.AlarmSubExpression;
import com.hpcloud.mon.common.model.metric.Metric;
import com.hpcloud.mon.common.model.metric.MetricDefinition;
import com.hpcloud.streaming.storm.TopologyTestCase;
import com.hpcloud.util.Injector;

import backtype.storm.Config;
import backtype.storm.testing.FeederSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

import com.google.common.collect.ImmutableMap;
import com.google.inject.AbstractModule;

import monasca.thresh.domain.model.MetricDefinitionAndTenantId;
import monasca.thresh.domain.model.SubAlarm;
import monasca.thresh.domain.service.AlarmDAO;
import monasca.thresh.domain.service.AlarmDefinitionDAO;
import monasca.thresh.infrastructure.thresholding.AlarmEventForwarder;
import monasca.thresh.infrastructure.thresholding.MetricAggregationBolt;
import monasca.thresh.infrastructure.thresholding.MetricSpout;
import monasca.thresh.infrastructure.thresholding.ProducerModule;

import org.testng.annotations.Test;

import java.util.Arrays;

/**
 * Simulates a real'ish run of the thresholding engine, using seconds instead of minutes for the
 * evaluation timescale.
 */
@Test(groups = "integration")
public class ThresholdingEngineTest1 extends TopologyTestCase {
  private static final String JOE_TENANT_ID = "joe";
  private static final String BOB_TENANT_ID = "bob";
  private FeederSpout metricSpout;
  private FeederSpout eventSpout;
  private AlarmDAO alarmDAO;
  private AlarmDefinitionDAO alarmDefinitionDAO;
  private MetricDefinition cpuMetricDef;
  private MetricDefinition memMetricDef;
  private MetricDefinition customMetricDef;

  private AlarmExpression expression;
  private AlarmExpression customExpression;
  private AlarmSubExpression customSubExpression;

  public ThresholdingEngineTest1() {
    // Fixtures
    expression =
        new AlarmExpression(
            "avg(hpcs.compute.cpu{id=5}, 3) >= 3 times 2 and avg(hpcs.compute.mem{id=5}, 3) >= 5 times 2");
    customExpression = AlarmExpression.of("avg(my.test{id=4}, 3) > 10");
    customSubExpression = customExpression.getSubExpressions().get(0);

    cpuMetricDef = expression.getSubExpressions().get(0).getMetricDefinition();
    memMetricDef = expression.getSubExpressions().get(1).getMetricDefinition();
    customMetricDef = customSubExpression.getMetricDefinition();

    // Mocks
    alarmDAO = mock(AlarmDAO.class);
    /* FIX THIS
    when(alarmDAO.findById(anyString())).thenAnswer(new Answer<Alarm>() {
      @Override
      public Alarm answer(InvocationOnMock invocation) throws Throwable {
        if (invocation.getArguments()[0].equals("1")) {
          return new Alarm("1", BOB_TENANT_ID, "test-alarm", "Descr of test-alarm", expression,
              Arrays.asList(createCpuSubAlarm(), createMemSubAlarm()), AlarmState.OK, Boolean.TRUE);
        } else if (invocation.getArguments()[0].equals("2")) {
          return new Alarm("2", JOE_TENANT_ID, "joes-alarm", "Descr of joes-alarm",
              customExpression, Arrays.asList(createCustomSubAlarm()), AlarmState.OK, Boolean.TRUE);
        }
        return null;
      }
    });
    */

    alarmDefinitionDAO = mock(AlarmDefinitionDAO.class);

    /* FIX THIS
    metricDefinitionDAO = mock(MetricDefinitionDAO.class);
    final List<SubAlarmMetricDefinition> metricDefs =
        Arrays.asList(new SubAlarmMetricDefinition(createCpuSubAlarm().getId(),
            new MetricDefinitionAndTenantId(cpuMetricDef, BOB_TENANT_ID)),
            new SubAlarmMetricDefinition(createMemSubAlarm().getId(),
                new MetricDefinitionAndTenantId(memMetricDef, BOB_TENANT_ID)),
            new SubAlarmMetricDefinition(createCustomSubAlarm().getId(),
                new MetricDefinitionAndTenantId(customMetricDef, JOE_TENANT_ID)));
    when(metricDefinitionDAO.findForAlarms()).thenReturn(metricDefs);
    */

    // Bindings
    Injector.reset();
    Injector.registerModules(new AbstractModule() {
      protected void configure() {
        bind(AlarmDAO.class).toInstance(alarmDAO);
        bind(AlarmDefinitionDAO.class).toInstance(alarmDefinitionDAO);
      }
    });

    // Config
    ThresholdingConfiguration threshConfig = new ThresholdingConfiguration();
    Config stormConfig = new Config();
    stormConfig.setMaxTaskParallelism(5);

    metricSpout = new FeederSpout(new Fields(MetricSpout.FIELDS));
    eventSpout = new FeederSpout(new Fields("event"));
    final AlarmEventForwarder alarmEventForwarder = mock(AlarmEventForwarder.class);

    Injector
        .registerModules(new TopologyModule(threshConfig, stormConfig, metricSpout, eventSpout));
    Injector.registerModules(new ProducerModule(alarmEventForwarder));

    // Evaluate alarm stats every 1 seconds
    System.setProperty(MetricAggregationBolt.TICK_TUPLE_SECONDS_KEY, "1");
  }

  private SubAlarm createCpuSubAlarm() {
    return new SubAlarm("111", "1", expression.getSubExpressions().get(0));
  }

  private SubAlarm createMemSubAlarm() {
    return new SubAlarm("222", "1", expression.getSubExpressions().get(1));
  }

  private SubAlarm createCustomSubAlarm() {
    return new SubAlarm("333", "2", customSubExpression);
  }

  public void shouldThreshold() throws Exception {
    int count = 0;
    int eventCounter = 0;

    while (true) {
      long time = System.currentTimeMillis();
      metricSpout.feed(new Values(new MetricDefinitionAndTenantId(cpuMetricDef, BOB_TENANT_ID),
          new Metric(cpuMetricDef.name, cpuMetricDef.dimensions, time, count % 10 == 0 ? 555 : 1)));
      metricSpout.feed(new Values(new MetricDefinitionAndTenantId(memMetricDef, BOB_TENANT_ID),
          new Metric(memMetricDef.name, cpuMetricDef.dimensions, time, count % 10 == 0 ? 555 : 1)));
      metricSpout
          .feed(new Values(new MetricDefinitionAndTenantId(customMetricDef, JOE_TENANT_ID),
              new Metric(customMetricDef.name, cpuMetricDef.dimensions, time, count % 20 == 0 ? 1
                  : 123)));

      if (count % 5 == 0) {
        Object event = null;
        if (++eventCounter % 2 == 0) {
          event =
              new AlarmDefinitionDeletedEvent("2", ImmutableMap
                  .<String, MetricDefinition>builder().put("444", customMetricDef).build());
        } else {
          // TODO - Make sure this makes sense
          event =
              new AlarmDefinitionCreatedEvent(JOE_TENANT_ID, "2", "foo", "foo description",
                  customSubExpression.getExpression(), ImmutableMap
                      .<String, AlarmSubExpression>builder().put("444", customSubExpression)
                      .build(), Arrays.asList("hostname"));
        }

        eventSpout.feed(new Values(event));
      }

      try {
        Thread.sleep(1000);
      } catch (InterruptedException e) {
        return;
      }

      count++;
    }
  }
}