require 'ipaddr'

def register(params)
	@inner_ips = params["inner_ips"].split(',')
	@inner_ips.each_index do |index|
		inner_ip_range = @inner_ips[index].split('-')
		if inner_ip_range.size == 2
			inner_start = ip_to_number(inner_ip_range[0])
			inner_end = ip_to_number(inner_ip_range[1])
			@inner_ips[index] = [inner_start, inner_end]
		else
			inner_ip = ip_to_number(inner_ip_range[0])
			@inner_ips[index] = [inner_ip, inner_ip]
		end
	end
end

def ip_to_number(ip)
	begin
		ip_num = IPAddr.new ip
		return ip_num.to_i
	rescue => e
		puts("IP address parse failed. IP: #{ip}, Message: #{e.message}")
		return 0
	end
end

def is_inner_ip(ip_num)
	@inner_ips.each do |item|
		if ip_num >= inner_start and ip_num <= inner_end
			return true
		end
	end

	return false
end

def filter(event)
	ip = event.get('ip')
	if ip.nil? or ip.empty?
		event.tag('_ip_lookup_failure')
		return [ event ]
	end

	ip_num = ip_to_number(ip)
	if ip_num == 0
		event.tag('_ip_lookup_failure')
		return [ event ]
	end

	inner = is_inner_ip(ip_num)
	event.set('ip_num', ip_num)
	event.set('inner', inner)
	
	return [ event ]
end
