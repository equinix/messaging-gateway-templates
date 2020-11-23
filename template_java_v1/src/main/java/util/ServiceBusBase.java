/** EQUINIX MESSAGING GATEWAY TEMPLATE **/

/*************************************************************************
 *
 * EQUINIX CONFIDENTIAL
 * __________________
 *
 *  © 2020 Equinix, Inc. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Terms of Use: https://www.equinix.com/company/legal/terms/
 *
 *************************************************************************/

package util;

import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import org.json.JSONObject;
import config.*;

public class ServiceBusBase {
	public static void sendMessageToQueue(JSONObject payload, String label) throws Exception {

		String connectionString = config.EQUINIX_INCOMING_QUEUE_CONNECTION_STRING;
		String queueName = config.EQUINIX_INCOMING_QUEUE;
		JSONObject body = (JSONObject) payload.get("Task");
		payload.remove("Task");
		payload.put("Task", body.toString());

		ServiceBusSenderClient sender = new ServiceBusClientBuilder()
				.connectionString(connectionString)
				.sender()
				.queueName(queueName)
				.buildClient();
		sender.sendMessage(new ServiceBusMessage(payload.toString().getBytes("utf-8")));
		sender.close();
	}
}